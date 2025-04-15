import copy
from typing import List, Set, Tuple, Dict

class ParseJson():  
    def __init__(self, data):
        self.data = data
        self.result = {}
        
    def find_key_in_item(self, item, key_path) -> Dict[str, any]:
        found_val = item
        for segment in key_path:
            if type(found_val) is not dict: return None
            val = found_val.get(segment, None)
            if val:
                found_val = val
        return found_val if found_val != item else None
        
    def reorganize_by_key_path(self, key_path: str) -> Dict[str, any]:
        if not key_path or not str.strip(key_path, ' .'):
            return {}
        key_path = key_path.split(".")
        for item in self.data.values():
            key = self.find_key_in_item(item, key_path)
            if not key: continue
            cur_value_at_key = self.result.get(key, None)
            if not cur_value_at_key:
                self.result[key] = item
                continue
            if not isinstance(cur_value_at_key, list):
                self.result[key] = [cur_value_at_key, item]
                continue
            self.result[key].append(item)
        return self.result

    def _add_to_object(self, new_obj: any, cur_obj: any) -> None:
        if not isinstance(new_obj, dict): return
        for k, new_v in new_obj.items():
            if k in cur_obj:
                cur_v = cur_obj[k]
                cur_v_type = type(cur_v)
                new_v_type = type(new_v)
                if cur_v_type == new_v_type:
                    if cur_v_type in [dict, set]:
                        new_v.update(cur_v)
                        self._add_to_object(new_v, cur_v)
                    elif cur_v_type == list:
                        new_v.extend(cur_v)
                    else:
                        new_v = [new_v, cur_v]
            else:
                cur_obj[k] = new_v
        
    def add_to_data(self, items: Dict[str, any]) -> Dict[str, any]:
        for k, v in items.items():
            if k in self.data:
                self._add_to_object(v, self.data[k])
                continue
            self.data[k] = v
        return self.data

class TestClass:
    def __init__(self):
        self.data1 = {
            "point2": {
                "d1": "goodbye",
                "d2": 5,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjhdas"
                }
            }
        }

        self.data2 = {
            "point1": {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs",
                    "ed3": {
                        "hi": 3
                    }
                }
            }
        }

        self.default_json_parser = ParseJson(copy.deepcopy(self.data1))
        self.json_parser_2 = ParseJson(copy.deepcopy(self.data2))

        self.add_to_data2_res = {
            "point1": {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs",
                    "ed3": {
                        "hi": 3
                    },
                    "ed4": 220
                }
            }
        }

        self.add_to_data1_res = {
            "point1": {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs"
                }
            },
            "point2": {
                "d1": "goodbye",
                "d2": 5,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjhdas"
                }
            },
            "point3": {
                "d2": 100,
                "d3": {
                    "ed1": 2
                }
            },
            "hi": "hello"
        }

    def test_find_key_in_item(self):
        obj = self.data1["point2"]
        parser = self.default_json_parser
        assert parser.find_key_in_item(obj, ["d3","ed1"]) == 1
        assert parser.find_key_in_item(obj, ["d1"]) == "goodbye"
        assert parser.find_key_in_item(obj, ["d4"]) is None

    def test_add_to_data(self):
        parser = self.json_parser_2
        test_input = {
            "point1": {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs",
                    "ed3": 7,
                    "ed4": 220
                }
            }
        }
        assert parser.add_to_data(test_input) == self.add_to_data2_res

        parser = self.default_json_parser
        new_item = {"hi": "hello"}
        expected_data = copy.deepcopy(self.data1)
        expected_data["hi"] = "hello"
        assert parser.add_to_data(new_item) == expected_data

        new_items = {
            "point1": {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs"
                }
            },
            "point3": {
                "d2": 100,
                "d3": {
                    "ed1": 2
                }
            }
        }
        assert parser.add_to_data(new_items) == self.add_to_data1_res

    def test_reorganize_by_key_path(self):
        parser = ParseJson({
            "point1": {
                "d1": "goodbye",
                "d2": 5,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjhdas"
                }
            },
            "point2": {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs"
                }
            },
            "point3": {
                "d2": 100,
                "d3": {
                    "ed1": 2
                }
            }
        })

        expected = {
            1: [
                {
                    "d1": "goodbye",
                    "d2": 5,
                    "d3": {
                        "ed1": 1,
                        "ed2": "asjhdas"
                    }
                },
                {
                    "d1": "hello",
                    "d2": 10,
                    "d3": {
                        "ed1": 1,
                        "ed2": "asjdlkajs"
                    }
                }
            ],
            2: {
                "d2": 100,
                "d3": {
                    "ed1": 2
                }
            }
        }
        assert parser.reorganize_by_key_path("d3.ed1") == expected

        parser = ParseJson(copy.deepcopy(self.add_to_data2_res))
        expected_nested = {
            3: {
                "d1": "hello",
                "d2": 10,
                "d3": {
                    "ed1": 1,
                    "ed2": "asjdlkajs",
                    "ed3": {
                        "hi": 3
                    },
                    "ed4": 220
                }
            }
        }
        assert parser.reorganize_by_key_path("d3.ed3.hi") == expected_nested
        
    def test_invalid_key_paths(self):
        parser = self.default_json_parser
        assert parser.reorganize_by_key_path("") == {}
        assert parser.reorganize_by_key_path(None) == {}
        assert parser.reorganize_by_key_path(".") == {}
        assert parser.reorganize_by_key_path("nonexistent.key.path") == {}

if __name__ == "__main__":    
    test_class = TestClass()
    test_class.test_find_key_in_item()
    test_class.test_add_to_data()
    test_class.test_reorganize_by_key_path()
    test_class.test_invalid_key_paths()
        