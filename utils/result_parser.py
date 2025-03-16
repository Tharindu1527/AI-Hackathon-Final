# utils/result_parser.py (updated)

import re

def parse_crew_result(raw_result):
    # Initialize the structured result
    structured_result = {
        "summary": "",
        "key_topics": [],
        "sentiment_analysis": "",
        "action_items": []
    }
    
    # Check if the result appears to be a direct list of action items (without headers)
    if raw_result and raw_result.strip().startswith("1.") and "**" in raw_result:
        print("Detected direct numbered list format, parsing as action items")
        
        # The first paragraph before the numbered list can be treated as a summary
        summary_end = raw_result.find("1. **")
        if summary_end > 0:
            structured_result["summary"] = raw_result[:summary_end].strip()
        
        # Parse the action items
        structured_result["action_items"] = extract_numbered_list_items(raw_result)
        
        # Extract sentiment info if present
        if "sentiment analysis" in raw_result.lower():
            sentiment_start = raw_result.lower().find("sentiment analysis")
            sentiment_end = raw_result.find("1. **", sentiment_start)
            if sentiment_end > sentiment_start:
                structured_result["sentiment_analysis"] = raw_result[sentiment_start:sentiment_end].strip()
        
        # Extract topics if they can be inferred from action items
        # (This is a heuristic approach - you might need to adjust)
        topics = set()
        for item in structured_result["action_items"]:
            # Extract key concepts from action items
            words = item.split()
            if len(words) >= 2:
                topics.add(" ".join(words[:2]))
        
        structured_result["key_topics"] = list(topics)
        
        return structured_result

def extract_section(text, section_name, next_sections=None):
    """
    Extract a specific section from the raw text result
    
    Args:
        text: Raw text to parse
        section_name: Name of the section to extract (e.g., "Executive Summary")
        next_sections: List of names of sections that could follow this one
        
    Returns:
        str: Extracted section text or empty string if not found
    """
    # Handle case variations in section name
    patterns = [
        f"{section_name}:",
        f"{section_name.upper()}:",
        f"# {section_name}",
        f"## {section_name}",
        f"**{section_name}**",
        f"*{section_name}*"
    ]
    
    # Try each pattern
    section_text = ""
    for pattern in patterns:
        if pattern in text:
            # Get the part after this pattern
            parts = text.split(pattern, 1)
            if len(parts) > 1:
                section_text = parts[1].strip()
                break
    
    # If section was found, find the end of the section
    if section_text:
        end_pos = len(section_text)
        
        # Look for the next section markers
        if next_sections:
            for next_section in next_sections:
                for pattern in [
                    f"{next_section}:",
                    f"{next_section.upper()}:",
                    f"# {next_section}",
                    f"## {next_section}",
                    f"**{next_section}**",
                    f"*{next_section}*"
                ]:
                    if pattern in section_text:
                        pattern_pos = section_text.find(pattern)
                        if pattern_pos < end_pos:
                            end_pos = pattern_pos
        
        # Extract the section up to the identified end position
        section_text = section_text[:end_pos].strip()
    
    return section_text

def extract_bullet_points(text):
    """
    Extract bullet points from text
    
    Args:
        text: Text containing bullet points
        
    Returns:
        list: List of bullet points
    """
    if not text:
        return []
    
    # Split text into lines
    lines = text.split('\n')
    bullet_points = []
    
    # Process each line
    for line in lines:
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Check if line starts with bullet point markers
        if any(line.startswith(marker) for marker in ['-', '*', '•', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']):
            # Remove the bullet point marker
            clean_line = re.sub(r'^[-*•]|\d+\.\s*', '', line).strip()
            if clean_line:
                bullet_points.append(clean_line)
        else:
            # If not a bullet point but not empty, might be a continuation or standalone point
            if bullet_points:
                # Check if this might be a continuation of the previous point
                if len(line) < 50 and line[0].islower() and not line[0].isdigit():
                    bullet_points[-1] += " " + line
                else:
                    # Treat as a new point even without bullet marker
                    bullet_points.append(line)
            else:
                # First line without a bullet marker
                bullet_points.append(line)
    
    return bullet_points

def extract_numbered_list_items(text):
    """
    Extract items from a numbered list with detailed sub-points
    """
    if not text:
        return []
    
    items = []
    current_item = None
    in_item_details = False
    
    # Split by lines
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Check for numbered items like "1. **Title**"
        if re.match(r'^\d+\.\s+\*\*', line):
            # Save previous item if exists
            if current_item:
                items.append(current_item)
            
            # Extract title between ** markers
            title_match = re.search(r'\*\*([^*]+)\*\*', line)
            if title_match:
                current_item = title_match.group(1).strip()
            else:
                # Fallback if no ** formatting
                parts = line.split('.', 1)
                if len(parts) > 1:
                    current_item = parts[1].strip()
            
            in_item_details = True
        
        # Check for detail bullets like "- **Action:**"
        elif in_item_details and line.startswith('-') and '**' in line:
            # Extract the category (Action, Context, Benefit)
            category_match = re.search(r'\*\*([^:*]+):\*\*', line)
            if category_match and current_item:
                category = category_match.group(1).strip()
                # Extract the content after the category
                content = line.split(':', 1)[1].strip() if ':' in line else ""
                current_item += f" ({category}: {content})"
    
    # Add the last item
    if current_item:
        items.append(current_item)
    
    return items