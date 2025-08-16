from __future__ import annotations


class Item:
    """Represents an item type."""

    def __init__(self, item_id: str, name: str, *, stackable: bool = True) -> None:
        self.id = item_id
        self.name = name
        self.stackable = stackable


class Inventory:
    """Simple inventory that tracks item quantities by ID."""

    def __init__(self) -> None:
        # key: item_id, value: quantity
        self.slots: dict[str, int] = {}

    def add(self, item_id: str, qty: int) -> None:
        """Add an item to the inventory."""
        if qty <= 0:
            return
        self.slots[item_id] = self.slots.get(item_id, 0) + qty
        print(f"Added {qty}x {item_id} (total: {self.slots[item_id]})")

    def remove(self, item_id: str, qty: int) -> bool:
        """Remove an item from the inventory. Returns True if successful."""
        if item_id not in self.slots or qty <= 0:
            return False
        current = self.slots[item_id]
        if qty > current:
            return False
        if qty == current:
            del self.slots[item_id]
        else:
            self.slots[item_id] = current - qty
        print(f"Removed {qty}x {item_id} (remaining: {self.slots.get(item_id, 0)})")
        return True

    def count(self, item_id: str) -> int:
        """Return the quantity of the given item."""
        return self.slots.get(item_id, 0)

    def has(self, item_id: str, qty: int = 1) -> bool:
        """Check if inventory has at least `qty` of `item_id`."""
        return self.count(item_id) >= qty
    
    def return_all_items(self) -> dict[str, int]:
        """Return a dictionary of all items with their quantities."""
        return self.slots.copy()

    def __repr__(self) -> str:
        return f"Inventory({self.slots})"
