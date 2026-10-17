#!/usr/bin/env python3
import json
import sys
from client import EnterpriseComplianceDataRetentionErasureSentinel

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sentinel = EnterpriseComplianceDataRetentionErasureSentinel()
        stores = [
            {"store_name": "postgres_users_table", "records_count": 14, "contains_pii": True},
            {"store_name": "qdrant_vector_memory", "records_count": 48, "contains_pii": True}
        ]
        res = sentinel.execute_gdpr_erasure_workflow("USR-5501", stores)
        assert res["erasure_status"] == "ERASURE_EXECUTED_COMPLIANT"
        assert res["proof_certificate"] is not None
        print(f"[TEST PASS] GDPR Erasure Executed: Cert ID {res['proof_certificate']['certificate_id']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-gdpr-erasure-sentinel", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "execute_gdpr_erasure_workflow", "description": "GDPR right-to-be-forgotten erasure sentinel"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                sentinel = EnterpriseComplianceDataRetentionErasureSentinel()
                out = sentinel.execute_gdpr_erasure_workflow(args.get("subject_id", ""), args.get("data_stores", []), args.get("active_legal_holds"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
