import json
import requests
from langchain_tavily import TavilySearch

class NominatimPlaceSearchTool:
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    USER_AGENT = "AI-Trip-Planner/1.0 (contact@example.com)"

    def _search(self, query: str):
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": 5,
        }
        headers = {"User-Agent": self.USER_AGENT}
        response = requests.get(self.BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            return [f"No results found for '{query}'"]
        return [self._format_place(item) for item in data]

    def _format_place(self, item: dict) -> str:
        name = item.get("display_name", "Unknown location")
        lat = item.get("lat")
        lon = item.get("lon")
        return f"{name} (lat={lat}, lon={lon})"

    def search_attractions(self, place: str):
        return self._search(f"attractions in {place}")

    def search_restaurants(self, place: str):
        return self._search(f"restaurants in {place}")

    def search_activity(self, place: str):
        return self._search(f"things to do in {place}")

    def search_transportation(self, place: str):
        return self._search(f"transportation options in {place}")

class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str):
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_restaurants(self, place: str):
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_activity(self, place: str):
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str):
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    