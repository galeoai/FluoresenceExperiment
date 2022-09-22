import re, cv2, os
from typing import List, Tuple


class Sample:
    def __init__(self, filenames: List[str]):
        self.ET470_unlit_name, filenames = self.filter(filenames, ["470", "W.O.LIGHT"])
        self.ET505_unlit_name, filenames = self.filter(filenames, ["505", "W.O.LIGHT"])
        self.ET545_unlit_name, filenames = self.filter(filenames, ["545", "W.O.LIGHT"])
        self.ET470_lit_name, filenames = self.filter(filenames, ["470"])
        self.ET505_lit_name, filenames = self.filter(filenames, ["505"])
        self.ET545_lit_name, filenames = self.filter(filenames, ["545"])

    def load(self):
        self.ET470_unlit = cv2.imread(os.path.join("data", self.ET470_unlit_name))
        self.ET505_unlit = cv2.imread(os.path.join("data", self.ET505_unlit_name))
        self.ET545_unlit = cv2.imread(os.path.join("data", self.ET545_unlit_name))
        self.ET470_lit = cv2.imread(os.path.join("data", self.ET470_lit_name))
        self.ET505_lit = cv2.imread(os.path.join("data", self.ET505_lit_name))
        self.ET545_lit = cv2.imread(os.path.join("data", self.ET545_lit_name))

    def unload(self):
        del self.ET470_unlit
        del self.ET505_unlit
        del self.ET545_unlit
        del self.ET470_lit
        del self.ET505_lit
        del self.ET545_lit

    def filter(self, names: List[str], search_tokens: List[str]) -> Tuple[str, List[str]]:
        patterns = [re.compile(token) for token in search_tokens]
        matches = []
        for i in range(len(names)):
            found = True
            for pat in patterns:
                if not pat.search(names[i]):
                    found = False
                    break
            if found:
                matches.append(i)
        if len(matches) != 1:
            raise RuntimeError(f"Cannot solve Sample names. Found {len(matches)}, ({matches}) samples for phrases {search_tokens} for {names}")
        else:
            ret = names[matches[0]]
            del[names[matches[0]]]
            return ret, names
    
    def all_filenames(self) -> List[str]:
        return [self.ET470_unlit_name,
                     self.ET505_unlit_name,
                     self.ET545_unlit_name, 
                     self.ET470_lit_name, 
                     self.ET505_lit_name,
                     self.ET545_lit_name]

    def all_imgs(self):
        return [self.ET470_unlit, self.ET505_unlit, self.ET545_unlit, self.ET470_lit, self.ET505_lit, self.ET545_lit]
