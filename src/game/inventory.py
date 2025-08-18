from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.world import World


class Item:
    """Represents an item type."""

    def __init__(self, item_id: str, name: str, *, stackable: bool = False) -> None:
        self.id = item_id
        self.name = name
        self.stackable = stackable
        self.image_url = None


class Inventory:
    """Inventory for non-stackable items keyed by item.id."""

    def __init__(self) -> None:
        self.slots: dict[str, "Item"] = {}  # key = item.id, value = item object

    def add(self, item: "Item") -> None:
        # Each item is unique, keyed by id
        self.add_image(item)
        self.slots[item.id] = item
        print(f"Added {item.name} (id={item.id})")

    def remove(self, item: "Item") -> bool:
        if len(self.slots) == 0:
            print("Inventory is empty, cannot remove item.")
            return False
        if item.id not in self.slots:
            return False
        del self.slots[item.id]
        print(f"Removed {item.name} (id={item.id})")
        return True

    def count(self) -> int:
        return len(self.slots)
    
    def add_image(self, item: Item) -> None:
        """Add an image URL to the item."""
        if item.name == "fruit":
            item.image_url = "assets/sprites/fruit.png"

    def has_fruit(self, name="fruit") -> bool:
        if len(self.slots) == 0:
            return False
        for slot_item in self.slots.values():
            if slot_item.name == name:
                return True
            
    def remove_fruit(self, world: "World", name="fruit") -> bool:
        """Remove a fruit item from the inventory."""
        print(f"Attempting to remove {name} from inventory.")
        if not self.has_fruit(name):
            print("No fruit in inventory to remove.")
            return False
        for item_id, item in list(self.slots.items()):
            if item.name == name:
                del self.slots[item_id]
                print(self.slots)
                return True
        return False
    
        
    
    def return_all_items(self) -> dict[int, "Item"]:
        return dict(self.slots)

    def __repr__(self) -> str:
        return f"Inventory({self.slots})"
