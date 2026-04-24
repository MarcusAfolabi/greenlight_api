from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.user import User, UserRole
from app.schemas.organization import OrganizationCreate
from app.schemas.user import UserCreate
from app.core.security import hash_password 

class OrganizationService:
    """Service layer for organization and host onboarding."""

    @staticmethod
    def get_by_subdomain(db: Session, subdomain: str) -> Organization | None:
        return db.query(Organization).filter(Organization.subdomain == subdomain).first()

    @staticmethod
    def create_organization(
        db: Session, organization_data: OrganizationCreate, owner_id: int
    ) -> Organization:
        organization = Organization(
            name=organization_data.name,
            subdomain=organization_data.subdomain,
            industry=organization_data.industry,
            owner_id=owner_id,
        )
        db.add(organization)
        db.flush()
        return organization

    @staticmethod
    def create_host_with_organization(db: Session, user_data: UserCreate) -> User:
        if user_data.organization is None:
            raise ValueError("Organization data is required for host registration")

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            role=UserRole.HOST,
        )
        db.add(user)
        db.flush()

        OrganizationService.create_organization(db, user_data.organization, user.id)

        db.commit()
        db.refresh(user)
        return user
 
organization_service = OrganizationService()