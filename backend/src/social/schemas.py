from pydantic import BaseModel, root_validator
from pytils.translit import slugify


class PostCreate(BaseModel):
    title: str
    text: str
    slug: str

    @root_validator(pre=True)
    def generate_slug(values):
        if 'title' in values:
            values['slug'] = slugify(values.get("title"))
        return values
