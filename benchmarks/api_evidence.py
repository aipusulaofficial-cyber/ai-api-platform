import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_domain import TokenBucket,validate_version
validate_version("v1"); b=TokenBucket(2,1); results=[b.consume(now=0),b.consume(now=0),b.consume(now=0),b.consume(now=1)]
report={"version_valid":True,"token_results":results}
if results!=[True,True,False,True]: raise SystemExit(report)
print(json.dumps(report,sort_keys=True))
