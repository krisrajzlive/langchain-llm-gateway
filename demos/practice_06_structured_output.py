"""Structured (schema-constrained) output via `with_structured_output`.

The gateway returns a validated Pydantic instance instead of raw text,
regardless of whether the underlying provider natively supports function
calling / JSON mode.
"""

from pydantic import BaseModel, Field

from gateway import get_model


class MovieReview(BaseModel):
    title: str = Field(description="Title of the movie")
    rating_out_of_10: int = Field(description="Rating from 1 to 10")
    one_line_summary: str = Field(description="A one-sentence summary")


def main() -> None:
    model = get_model("openai:gpt-4o-mini")
    structured_model = model.with_structured_output(MovieReview)

    result = structured_model.invoke(
        "Review the movie 'The Matrix' in the requested schema."
    )
    print(result)


if __name__ == "__main__":
    main()
