from __future__ import annotations


class Item:
    """Represents an item type."""

    def __init__(self, item_id: str, name: str, *, stackable: bool = True) -> None:
        self.id = item_id
        self.name = name
        self.stackable = stackable


class Inventory:
    """Inventory keyed by Item objects directly."""

    def __init__(self) -> None:
        self.slots: dict[Item, int] = {}

    def add(self, item: Item, qty: int) -> None:
        if qty <= 0:
            return
        self.slots[item] = self.slots.get(item, 0) + qty
        print(f"Added {qty}x {item.name} (total: {self.slots[item]})")

    def remove(self, item: Item, qty: int) -> bool:
        if item not in self.slots or qty <= 0:
            return False
        current = self.slots[item]
        if qty > current:
            return False
        if qty == current:
            del self.slots[item]
        else:
            self.slots[item] = current - qty
        print(f"Removed {qty}x {item.name} (remaining: {self.slots.get(item, 0)})")
        return True

    def count(self, item: Item) -> int:
        return self.slots.get(item, 0)

    def has(self, item: Item, qty: int = 1) -> bool:
        return self.count(item) >= qty

    def return_all_items(self) -> dict[str, int]:
        return {item.name: qty for item, qty in self.slots.items()}

    def __repr__(self) -> str:
        return f"Inventory({self.return_all_items()})"
