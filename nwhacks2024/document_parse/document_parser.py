import os
from io import StringIO
from typing import Annotated, Any, Iterable

import instructor
import pandas as pd
from openai import OpenAI
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    InstanceOf,
    PlainSerializer,
    WithJsonSchema,
)
from utils import md_to_df

MarkdownDataFrame = Annotated[
    InstanceOf[pd.DataFrame],
    BeforeValidator(md_to_df),
    PlainSerializer(lambda df: df.to_markdown()),
    WithJsonSchema(
        {
            "type": "string",
            "description": """The markdown representation of the table, each one should be tidy, do not try to join tables that should be seperate. 
            The tables are menus, so keep that in mind when parsing them.
            Tables should have a title, description, price, and dietary restrictions column if applicable.""",
        }
    ),
]


class Table(BaseModel):
    caption: str
    dataframe: MarkdownDataFrame


try:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY_NWHACKS2024"]
except:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY_NWHACKS2024")

# Apply the patch to the OpenAI client to support response_model
# Also use MD_JSON mode since the vision model does not support any special structured output mode
client = instructor.patch(
    OpenAI(api_key=OPENAI_API_KEY), mode=instructor.function_calls.Mode.MD_JSON
)


def extract_table(url: str) -> Iterable[Table]:
    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=Iterable[Table],
        max_tokens=1800,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Extract data fromthe table. Each one should be tidy, do not try to join tables that should be seperate. 
                                    The tables are menus, so keep that in mind when parsing them.
                                    Tables should have a title, description, price, and dietary restrictions column if applicable.""",
                    },
                    {"type": "image_url", "image_url": {"url": url}},
                ],
            }
        ],
    )


if __name__ == "__main__":
    url = input("Enter image url: ")
    for table in extract_table(url):
        print(table.caption)
        print(table.dataframe)
