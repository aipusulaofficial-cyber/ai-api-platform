from dataclasses import dataclass
import time

@dataclass(frozen=True)
class ApiRequest:
    request_id:str; version:str; key:str

class TokenBucket:
    def __init__(self,capacity:int,refill_per_s:float): self.capacity=capacity;self.tokens=float(capacity);self.rate=refill_per_s;self.last=time.monotonic()
    def consume(self,cost:int=1,now=None)->bool:
        now=time.monotonic() if now is None else now
        self.tokens=min(self.capacity,self.tokens+(now-self.last)*self.rate);self.last=now
        if self.tokens<cost:return False
        self.tokens-=cost;return True

def validate_version(version:str)->None:
    if version not in {"v1","v2"}: raise ValueError("unsupported api version")
