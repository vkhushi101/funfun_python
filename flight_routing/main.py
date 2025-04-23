
from collections import defaultdict
import heapq
import re
from typing import Dict, List, Optional, Tuple

class FlightRouter():
    def __init__(self, flights: List):
        self.flights = flights
        self.flight_dict = self.create_flight_dict()
    
    def create_flight_dict(self) -> None:
        flight_dict = defaultdict(dict)
        for flight in self.flights.split(","):
            flight_details: List = flight.split(":")
            source = flight_details.pop(0)
            destination = flight_details.pop(0)
            
            source_details = flight_dict[source]
            cost = flight_details[1]
            if destination in source_details and cost > source_details[destination][1]:
                continue
            if cost.isdigit():
                source_details[destination] = flight_details
        return flight_dict
        
    def find_cost_of_direct_flight(self, source: str, destination: str) -> Optional[int]:
        for dest, details in self.flight_dict[source].items():
            if dest == destination:
                return int(details[1])
        return None
    
    def find_cost_of_indirect_flights(self, source: str, destination: str) -> Tuple[any]:
        if source == destination:
            return ([source], 0)
        
        queue = []
        visited = [source]
        for k, v in self.flight_dict[source].items():
            heapq.heappush(queue, ([source, k], int(v[1])))
            visited.append(k)
        
        min_cost = None
        results = []
        
        while queue:
            path, cost = heapq.heappop(queue)
            source = path[-1]
            visited.append(source)
            
            for dest, details in self.flight_dict[source].items():
                if dest in visited:
                    continue
                
                path.append(dest)
                heapq.heappush(queue, (path, cost + int(details[1])))
                if dest != destination:
                    continue
                
                trip_cost = cost + int(details[1])
                if min_cost == None or trip_cost <= min_cost: 
                    min_cost = trip_cost
                    results.append(path)
                return (results, min_cost)
            
        return (results, None)

    def strip_stopwords(self, input: str, stopwords: List[str]) -> str:
        res = ' '.join(i if i.lower() not in stopwords else '' for i in input.split(' ')).lower().strip()
        return res if res != '' else None
        
    def sort_strings(self, strings: List[str]) -> List[str]:
        return sorted(strings, key=lambda x: (''.join([i for i in x if not i.isdigit()]), -int(''.join([i for i in x if i.isdigit()]))))

    def parse_http_request(self, request: str) -> Dict[str, str]:
        results_dict = {"param1": None, "param2": None}
        params = request.split("&")
        for i in params:
            if "param1" in i:
                results_dict['param1'] = i.split("param1")[1].strip('=') 
            if "param2" in i:
                results_dict['param2'] = i.split("param2")[1].strip('=') 
        return results_dict
        
    
if __name__ == "__main__":
    flights = "UK:US:FedEx:4,UK:FR:Jet1:2,US:UK:RyanAir:8,CA:UK:CanadaAir:8,US:IN:AirIndia:12,IN:AUS:AirAustralia:11"
    flight_router = FlightRouter(flights)
    
    assert flight_router.find_cost_of_direct_flight('UK', 'US') == 4  
    assert flight_router.find_cost_of_direct_flight('CA', 'UK') == 8
    assert flight_router.find_cost_of_direct_flight('US', 'FR') == None
    assert flight_router.find_cost_of_direct_flight('UK', 'UK') == None
    assert flight_router.find_cost_of_direct_flight('NonExistent', 'US') == None

    flight_router.flights = "UK:US:FedEx:4,UK:FR:Jet1:2,FR:DE:EasyFly:3,DE:US:Luft:5,CA:UK:CanadaAir:8"
    flight_router.flight_dict = flight_router.create_flight_dict()
    assert flight_router.find_cost_of_indirect_flights('CA', 'US') == ([['CA', 'UK', 'US']], 12)
    assert flight_router.find_cost_of_indirect_flights('UK', 'DE') == ([['UK', 'FR', 'DE']], 5)
    assert flight_router.find_cost_of_indirect_flights('US', 'CA') == ([], None)
    assert flight_router.find_cost_of_indirect_flights('UK', 'UK') == (['UK'], 0)
    assert flight_router.find_cost_of_indirect_flights('FR', 'US') == ([['FR', 'DE', 'US']], 8)
    assert flight_router.find_cost_of_indirect_flights('CA', 'NonExistent') == ([], None)

    flight_router.flights = "UK:US:United:2,UK:US:FedEx:4,UK:FR:Jet1:2,US:UK:RyanAir:8,CA:UK:CanadaAir:8,US:IN:AirIndia:12,IN:AUS:AirAustralia:11,FR:IN:AirFrance:8,IN:CAN:AirIndia:6"
    flight_router.flight_dict = flight_router.create_flight_dict()
    assert flight_router.find_cost_of_direct_flight('UK', 'US') == 2
    assert flight_router.find_cost_of_indirect_flights("UK","IN") == ([['UK', 'FR', 'IN']], 10)
    assert flight_router.find_cost_of_indirect_flights("US","FR") == ([['US', 'UK', 'FR']], 10)

    stop_words_list = ["is", "a", "to", "the", "and"]
    assert flight_router.strip_stopwords('This is a test sentence to remove stop words', stop_words_list) == "this   test sentence  remove stop words"
    assert flight_router.strip_stopwords('The quick brown fox jumps over the lazy dog', stop_words_list) == "quick brown fox jumps over  lazy dog"
    assert flight_router.strip_stopwords('No stop words here', stop_words_list) == "no stop words here"
    assert flight_router.strip_stopwords('IS A TO THE AND', stop_words_list) == None
    assert flight_router.strip_stopwords('Mixed Case Is A Test', stop_words_list) == "mixed case   test"
    assert flight_router.strip_stopwords('', stop_words_list) == None
    
    strings_list1 = ["a1", "b32", "caba522", "b21"]
    assert flight_router.sort_strings(strings_list1) == ['a1', 'b32', 'b21', 'caba522']
    strings_list2 = ["z9", "a10", "a2", "b5", "a1"]
    assert flight_router.sort_strings(strings_list2) == ['a10', 'a2', 'a1', 'b5', 'z9']
    strings_list3 = ["x1", "x10", "y5", "y1"]
    assert flight_router.sort_strings(strings_list3) == ['x10', 'x1', 'y5', 'y1']
    strings_list4 = ["abc10", "ab10", "abc20", "ab5"]
    assert flight_router.sort_strings(strings_list4) == ['ab10', 'ab5', 'abc20', 'abc10']
    strings_list5 = []
    assert flight_router.sort_strings(strings_list5) == []
    
    assert flight_router.parse_http_request('param1=123&param2=abc') == {'param1': '123', 'param2': 'abc'}
    assert flight_router.parse_http_request('param1=hello&param2=world') == {'param1': 'hello', 'param2': 'world'}
    assert flight_router.parse_http_request('param1=one&param2=two=extra') == {'param1': 'one', 'param2': 'two=extra'}
    assert flight_router.parse_http_request('param1=&param2=') == {'param1': '', 'param2': ''}
    assert flight_router.parse_http_request('param1=value1') == {'param1': 'value1', 'param2': None}
    assert flight_router.parse_http_request('param2=value2') == {'param1': None, 'param2': 'value2'}
    assert flight_router.parse_http_request('=value1&param2=value2') == {'param1': None, 'param2': 'value2'}
    assert flight_router.parse_http_request('param1=value1&') == {'param1': 'value1', 'param2': None}
    assert flight_router.parse_http_request('param1value1param2value2') == {'param1': 'value1param2value2', 'param2': 'value2'}
    assert flight_router.parse_http_request('') == {'param1': None, 'param2': None}
    assert flight_router.parse_http_request('param1=') == {'param1': '', 'param2': None}
    assert flight_router.parse_http_request('&param2=value2') == {'param1': None, 'param2': 'value2'}