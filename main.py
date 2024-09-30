from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationInfo
import os
import re
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PartidoModel(BaseModel):
    home_team: str = Field(..., min_length=1, max_length=30)
    away_team: str = Field(..., min_length=1, max_length=30)
    home_goals: int = Field(..., ge=0)
    away_goals: int = Field(..., ge=0)
    result: str = Field(..., min_length=1, max_length=3)
    season: str = Field(..., min_length=1, max_length=10)


    @field_validator("away_team")
    def different_teams(cls, away_team, info: ValidationInfo):
        home_team = info.data.get("home_team")
        if home_team and home_team == away_team:
            raise ValueError("El equipo local y el equipo visitante no pueden ser el mismo.")
        return away_team
    
    @field_validator("season")
    def validate_season_format(cls, season):
        pattern = r"^\d{4}-\d{4}$"
        if not re.match(pattern, season):
            raise ValueError("La temporada debe tener el formato 'YYYY-YYYY'.")
        return season


    class Config:
        orm_mode = True


class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    home_team = Column(String(30))
    away_team = Column(String(30))
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    result = Column(String(3))
    season = Column(String(10))

@app.get("/")
def read_root():
    return {"message": "Inicio"}

@app.get("/partidos/")
def read_partidos(db: Session = Depends(get_db), skip: int = 0, limit: int = Query(100, le=100)):
    partidos = db.query(Partido).offset(skip).limit(limit).all()
    total = db.query(Partido).count()
    return {"total": total, "Partidos": partidos, "skip": skip, "limit": limit}

@app.post("/partido/")
def crear_partidos(partidos: List[PartidoModel], db: Session = Depends(get_db)):
    partidos_agregados = 0

    try:
        for partido_info in partidos:
          
            partido = Partido(
                home_team=partido_info.home_team,
                away_team=partido_info.away_team,
                home_goals=partido_info.home_goals,
                away_goals=partido_info.away_goals,
                result=partido_info.result,
                season=partido_info.season
            )
            db.add(partido)
            partidos_agregados += 1

      
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al agregar partidos: {e}")

  
    total_partidos = db.query(Partido).count()

    return {"Partidos agregados": partidos_agregados, "Numero total de partidos": total_partidos}


@app.get("/partidos/filtrar/")
def filtrar_partidos(
    db: Session = Depends(get_db),
    temporada_exacta: str = Query(None, min_length=7, max_length=9, regex=r"^\d{4}-\d{4}$"),
    temporada_desde: str = Query(None, min_length=7, max_length=9, regex=r"^\d{4}-\d{4}$"),
    temporada_hasta: str = Query(None, min_length=7, max_length=9, regex=r"^\d{4}-\d{4}$"),
    skip: int = 0,
    limit: int = Query(100, le=100)
):
    # Validar que no se use temporada_exacta junto con temporada_desde o temporada_hasta
    if temporada_exacta and (temporada_desde or temporada_hasta):
        raise HTTPException(
            status_code=400,
            detail="No puedes usar temporada_exacta junto con temporada_desde o temporada_hasta. Elige uno de los dos."
        )

    query = db.query(Partido)

    # Filtrar por temporada exacta
    if temporada_exacta:
        query = query.filter(Partido.season == temporada_exacta)

    # Filtrar por rango de temporadas
    if temporada_desde and temporada_hasta:
        query = query.filter(and_(Partido.season >= temporada_desde, Partido.season <= temporada_hasta))
    elif temporada_desde:
        query = query.filter(Partido.season >= temporada_desde)
    elif temporada_hasta:
        query = query.filter(Partido.season <= temporada_hasta)

    # Obtener resultados con límite y paginación
    partidos = query.offset(skip).limit(limit).all()
    total = query.count()

    return {
        "total": total,
        "Partidos": partidos,
        "skip": skip,
        "limit": limit
    }












