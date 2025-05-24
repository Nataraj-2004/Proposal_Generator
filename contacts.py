# contacts.py

def format_contact(contact):
    """
    Formats a single contact into a readable string.
    Expects contact to be a dictionary with keys: name, role, email, phone.
    """
    return f"Name: {contact['name']}\nRole: {contact['role']}\nEmail: {contact['email']}\nPhone: {contact['phone']}"


def generate_contact_list(contacts, order_by="name"):
    """
    Generates and returns a sorted contact list.
    Args:
        contacts (list of dict): Each dict must have keys: name, role, email, phone.
        order_by (str): Field to sort contacts by ('name', 'role', etc.)
    Returns:
        List of formatted contact strings.
    """
    sorted_contacts = sorted(contacts, key=lambda x: x.get(order_by, ""))
    return [format_contact(c) for c in sorted_contacts]
