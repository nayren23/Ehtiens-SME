import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from ethiens_sme.service import seance_service

def test_pagination():
    print("Testing pagination...")
    
    # Fetch first page
    page1 = seance_service.get_upcoming_seances(limit=5, offset=0)
    print(f"Page 1 (Limit 5, Offset 0): {len(page1)} items")
    for s in page1:
        print(f" - ID: {s.get('seance_id')}, Date: {s.get('date_time')}")

    if not page1:
        print("No seances found, cannot test pagination overlap.")
        return

    # Fetch second page
    page2 = seance_service.get_upcoming_seances(limit=5, offset=5)
    print(f"\nPage 2 (Limit 5, Offset 5): {len(page2)} items")
    for s in page2:
        print(f" - ID: {s.get('seance_id')}, Date: {s.get('date_time')}")

    # Check for overlap
    ids1 = {s.get('seance_id') for s in page1}
    ids2 = {s.get('seance_id') for s in page2}
    
    intersection = ids1.intersection(ids2)
    
    if intersection:
        print(f"\nCRITICAL FAILURE: Found {len(intersection)} duplicate IDs between pages!")
        print(f"Duplicate IDs: {intersection}")
    else:
        print("\nSUCCESS: No duplicates found between pages.")

if __name__ == "__main__":
    test_pagination()
