import apache_beam as beam
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Any
from apache_beam.pvalue import TaggedOutput

class Location(BaseModel):
    address: str
    streetAddress: Optional[str] = None
    city: str
    country: Optional[str] = None
    postalCode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Hours(BaseModel):
    dayRange: str
    sectionHours: Optional[List[dict]] = None
 
class MenuItemModel(BaseModel):
    title: str
    titleBadge: Optional[str] = None
    itemDescription: Optional[str] = None
    price: int
    priceTagline: Optional[str] = None
    isSoldOut: Optional[bool] = None
    isAvailable: Optional[bool] = None
    hasCustomizations: Optional[bool] = None
    endorsement: Optional[str] = None
    labelPrimary: Optional[str] = None
    uuid: str
    rating: Optional[str] = None
    numRatings: Optional[int] = None
    
class Menu(BaseModel):
    catalogName: Optional[str] = None
    catalogItems: List[MenuItemModel]
    
class Rating(BaseModel):
    ratingValue: Optional[float] = None
    reviewCount: Optional[str] = None
    
class Distance(BaseModel):
    text: str
    accessibilityText: Optional[str] = None
    
class SupportedDiningModes(BaseModel):
    mode: str
    title: Optional[str]  = None
    isAvailable: Optional[bool] = None

class DataContract(BaseModel):
    
    title: str
    sanitizedTitle: Optional[str] = None
    phoneNumber: Optional[str] = None
    cuisineList : Optional[List[str]] = None
    location : Optional[Location] = None
    currencyCode : str
    rating : Optional[Rating] = None 
    storeAvailablityStatus : Optional[str] = None 
    isOpen : Optional [bool] = None  
    closedMessage: Optional[str] = None
    etaRange: Optional[str] = None
    hours : Hours
    categories : Optional[List[str]] = None
    categoriesLink: Optional[List[dict]] = None
    menu : Menu
    heroImageUrl : Optional[str] = None 
    uuid : Optional[str] = None
    url : Optional[str] = None
    distance : Distance
    supportedDiningModes : Optional[SupportedDiningModes] = None 
    storeReviews : List[Any] = []
    featuredReviews : List[Any] = []


class ValidateDataContract(beam.DoFn):
    
    OUTPUT_TAG_INVALID = 'invalid'
    
    def process(self, element):
        try:
            validated_model = DataContract.model_validate(element)
            
            first_menu_section = validated_model.menu[0] if validated_model.menu else None
            first_menu_item = first_menu_section.catalogItems[0] if first_menu_section and first_menu_section.catalogItems else None

            yield beam.Row(
                # --- Identification and Description ---
                restaurant_id=validated_model.uuid,
                name=validated_model.title,
                is_open=validated_model.isOpen,
                main_cuisine=validated_model.cuisineList[0] if validated_model.cuisineList else None,
                
                # --- Location  ---
                city=getattr(validated_model.location, 'city', None),
                country=getattr(validated_model.location, 'country', None),
                latitude=getattr(validated_model.location, 'latitude', None),
                longitude=getattr(validated_model.location, 'longitude', None),
                distance_text=getattr(validated_model.distance, 'text', None),

                # --- Performance and Operation ---
                rating_value=getattr(validated_model.rating, 'ratingValue', None),
                review_count=getattr(validated_model.rating, 'reviewCount', None),
                currency_code=validated_model.currencyCode,
                eta_range=validated_model.etaRange,
                menu_item_name_sample=getattr(first_menu_item, 'title', None),
                menu_item_price_sample=getattr(first_menu_item, 'price', None),
                menu_item_id_sample = getattr(first_menu_item, 'uuid', None),
                menu_item_rating_sample = getattr(first_menu_item, 'rating', None)
            )
            
        except ValidationError as e:
            error_record = {'original_data': element, 'error_message': str(e)}
            yield TaggedOutput(self.OUTPUT_TAG_INVALID, error_record)
        