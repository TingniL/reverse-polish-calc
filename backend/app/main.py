from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io, csv
import logging
from datetime import datetime

from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from . import schemas, crud, calculator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RPN Calculator API",
    description="""
    A Reverse Polish Notation (RPN) calculator API with history and CSV export.
    
    Example RPN expressions:
    - "2 3 +" = 5 (adds 2 and 3)
    - "2 3 4 + *" = 14 (adds 3 and 4, then multiplies result by 2)
    - "5 3 2 + *" = 25 (adds 3 and 2, then multiplies result by 5)
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4040"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")

@app.post("/calculate", response_model=schemas.OperationOut,
    description="Calculate result for a single RPN expression",
    response_description="Calculation result with expression history",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "simple": {
                            "value": {"expression": "2 3 +"}
                        },
                        "complex": {
                            "value": {"expression": "2 3 4 + *"}
                        }
                    }
                }
            }
        }
    }
)
def calculate(expr_in: schemas.ExpressionIn, db: Session = Depends(get_db)):
    logger.info(f"Processing expression: {expr_in.expression}")
    try:
        start_time = datetime.now()
        res = calculator.evaluate_rpn(expr_in.expression)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Calculation completed in {duration:.3f}s: {expr_in.expression} = {res}")
    except Exception as e:
        logger.error(f"Error calculating expression '{expr_in.expression}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    op = crud.create_operation(db, expr_in.expression, res)
    return op

async def process_expression(expr: str, db: Session):
    logger.info(f"Processing batch expression: {expr}")
    try:
        start_time = datetime.now()
        res = calculator.evaluate_rpn(expr)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Batch calculation completed in {duration:.3f}s: {expr} = {res}")
        crud.create_operation(db, expr, res)
    except Exception as e:
        logger.error(f"Error processing batch expression '{expr}': {str(e)}")

@app.post("/calculate_batch",
    description="Calculate results for multiple RPN expressions",
    response_description="Batch processing status",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "batch": {
                            "value": {
                                "expressions": [
                                    "2 3 +",
                                    "2 3 4 + *",
                                    "5 3 2 + *"
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
)
async def calculate_batch(
    expr_in: schemas.BatchExpressionIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.info(f"Starting batch processing of {len(expr_in.expressions)} expressions")
    
    # Validate all expressions first
    for expr in expr_in.expressions:
        try:
            calculator.evaluate_rpn(expr)
        except Exception as e:
            logger.error(f"Validation failed for expression '{expr}': {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid expression '{expr}': {str(e)}"
            )
    
    # Process all expressions asynchronously
    for expr in expr_in.expressions:
        background_tasks.add_task(process_expression, expr, db)
    
    logger.info(f"Batch processing started for {len(expr_in.expressions)} expressions")
    return {"message": f"Processing {len(expr_in.expressions)} expressions"}

@app.get("/history", response_model=list[schemas.OperationOut],
    description="Get calculation history",
    response_description="List of all calculations performed"
)
def history(db: Session = Depends(get_db)):
    logger.info("Retrieving calculation history")
    return crud.get_all_operations(db)

@app.get("/export_csv",
    description="Export calculation history as CSV",
    response_description="CSV file containing all calculations"
)
def export_csv(db: Session = Depends(get_db)):
    logger.info("Starting CSV export")
    ops = crud.get_all_operations(db)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "expression", "result", "created_at"])
    for o in ops:
        writer.writerow([o.id, o.expression, o.result, o.created_at])
    output.seek(0)
    logger.info(f"CSV export completed with {len(ops)} records")
    return StreamingResponse(output, media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=history.csv"})
