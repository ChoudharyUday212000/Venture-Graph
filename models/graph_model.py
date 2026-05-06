"""
Graph data model definitions and mappings
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum


class NodeType(Enum):
    """Node types in the graph"""
    COMPANY = "Company"
    INVESTOR = "Investor"
    FUND = "Fund"
    PERSON = "Person"
    SECTOR = "Sector"
    LOCATION = "Location"


class RelationType(Enum):
    """Relationship types in the graph"""
    LOCATED_IN = "LOCATED_IN"
    OPERATES_IN = "OPERATES_IN"
    INVESTED_IN = "INVESTED_IN"
    MANAGES = "MANAGES"
    COMMITS_TO = "COMMITS_TO"
    WORKS_AT = "WORKS_AT"
    WORKS_FOR = "WORKS_FOR"
    BOARD_MEMBER_OF = "BOARD_MEMBER_OF"
    KNOWS = "KNOWS"


@dataclass
class Company:
    """Company node model"""
    company_id: str
    name: str
    sector: str
    stage: str
    country: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "company_id": self.company_id,
            "name": self.name,
            "sector": self.sector,
            "stage": self.stage,
            "country": self.country,
        }


@dataclass
class Investor:
    """Investor node model"""
    investor_id: str
    name: str
    investor_type: str
    hq_country: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "investor_id": self.investor_id,
            "name": self.name,
            "investor_type": self.investor_type,
            "hq_country": self.hq_country,
        }


@dataclass
class Fund:
    """Fund node model"""
    fund_id: str
    name: str
    vintage: str
    strategy: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fund_id": self.fund_id,
            "name": self.name,
            "vintage": self.vintage,
            "strategy": self.strategy,
        }


@dataclass
class Person:
    """Person node model"""
    person_id: str
    name: str
    role: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "person_id": self.person_id,
            "name": self.name,
            "role": self.role,
        }


@dataclass
class Sector:
    """Sector node model"""
    sector_name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"sector_name": self.sector_name}


@dataclass
class Location:
    """Location node model"""
    location_name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"location_name": self.location_name}


@dataclass
class Relationship:
    """Generic relationship model"""
    rel_type: str
    from_node_id: str
    to_node_id: str
    properties: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rel_type": self.rel_type,
            "from_node_id": self.from_node_id,
            "to_node_id": self.to_node_id,
            "properties": self.properties or {},
        }
