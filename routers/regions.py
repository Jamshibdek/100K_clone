from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import crud
from schemas import schemas

router = APIRouter()

@router.post("/regions/", response_model=schemas.RegionOut)
def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
    return crud.create_region(db=db, region=region)

@router.get("/regions/", response_model=list[schemas.RegionOut])
def read_regions(db: Session = Depends(get_db)):
    return crud.get_regions(db=db)


@router.post("/districts/", response_model=schemas.DistrictOut)
def create_district(district: schemas.DistrictCreate, db: Session = Depends(get_db)):
    return crud.create_district(db=db, district=district)

@router.get("/districts/", response_model=list[schemas.DistrictOut])
def read_districts(db: Session = Depends(get_db)):
    return crud.get_districts(db=db)
