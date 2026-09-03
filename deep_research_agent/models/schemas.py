from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class ListSearchQuery(BaseModel):
    searches: list[SearchQuery] = Field(description="A list of web searches to perform.")


class SearchResult(BaseModel):
    query: str = Field(description="The search query that produced this result.")
    summary: str = Field(description="A concise summary of the findings for this query.")
    sources: list[str] = Field(default_factory=list, description="URLs or references backing the summary.")


class ResearchReport(BaseModel):
    answer: str = Field(description="The final, well-structured answer to the user's original query.")
    sources: list[str] = Field(default_factory=list, description="All sources cited across the research.")
