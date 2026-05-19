from utils.place_info_search import NominatimPlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool

class PlaceSearchTool:
    def __init__(self):
        self.nominatim_search = NominatimPlaceSearchTool()
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _serialize_results(self, results):
        if isinstance(results, list):
            return "\n".join(results)
        return str(results)

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                attraction_result = self.nominatim_search.search_attractions(place)
                return f"Attractions for {place}: {self._serialize_results(attraction_result)}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Nominatim search failed due to {e}.\nFallback attractions for {place}: {self._serialize_results(tavily_result)}"

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = self.nominatim_search.search_restaurants(place)
                return f"Restaurants for {place}: {self._serialize_results(restaurants_result)}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Nominatim search failed due to {e}.\nFallback restaurants for {place}: {self._serialize_results(tavily_result)}"

        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                activities_result = self.nominatim_search.search_activity(place)
                return f"Activities for {place}: {self._serialize_results(activities_result)}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Nominatim search failed due to {e}.\nFallback activities for {place}: {self._serialize_results(tavily_result)}"

        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                transportation_result = self.nominatim_search.search_transportation(place)
                return f"Transportation for {place}: {self._serialize_results(transportation_result)}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Nominatim search failed due to {e}.\nFallback transportation for {place}: {self._serialize_results(tavily_result)}"

        return [search_attractions, search_restaurants, search_activities, search_transportation]