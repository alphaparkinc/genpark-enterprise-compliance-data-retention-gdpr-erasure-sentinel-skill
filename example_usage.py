from client import EnterpriseComplianceDataRetentionErasureSentinel

def main():
    sentinel = EnterpriseComplianceDataRetentionErasureSentinel()
    stores = [
        {"store_name": "customer_relational_db", "records_count": 25},
        {"store_name": "vector_embedding_store", "records_count": 120},
        {"store_name": "analytics_event_logs", "records_count": 450}
    ]
    res = sentinel.execute_gdpr_erasure_workflow("CUST-EU-8821", stores)
    print("--- Enterprise GDPR Erasure Audit Output ---")
    print(f"Subject: {res['data_subject_id']} | Status: {res['erasure_status']}")
    print(f"Records Scrubbed: {res['total_records_scrubbed']}")
    print(f"Proof Certificate: {res['proof_certificate']['certificate_id']}")
    print(f"HMAC Digest: {res['proof_certificate']['hmac_sha256_proof'][:32]}...")

if __name__ == "__main__":
    main()
