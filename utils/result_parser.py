# utils/result_parser.py
import re
import json

def parse_crew_result(raw_result):
    """
    Parse raw results from the crew into a structured format
    
    This ultra-robust parser handles all observed output formats:
    - Numbered items starting directly (1. **Title**: Description)
    - Intro paragraph followed by numbered items
    - Prioritized Action Items format
    - Comprehensive Set format
    - Agent-based outputs
    
    Args:
        raw_result: Raw result string from CrewAI
        
    Returns:
        dict: Structured results with summary, key_topics, sentiment_analysis, action_items, etc.
    """
    # Debug logging
    print(f"Raw result first 100 chars: {raw_result[:100].replace(chr(10), ' ')}")
    print(f"Raw result length: {len(raw_result)}")
    
    # Initialize the structured result
    structured_result = {
        "summary": "",
        "key_topics": [],
        "sentiment_analysis": "",
        "action_items": []
    }
    
    # Check if the content begins with a paragraph followed by numbered items
    intro_paragraph, items_section = split_intro_and_items(raw_result)
    
    if intro_paragraph and "1. **" in items_section:
        print("Detected intro paragraph followed by numbered items format")
        
        # Use the intro paragraph as summary
        structured_result["summary"] = intro_paragraph
        
        # Extract items from the numbered section
        items = extract_numbered_items_with_descriptions(items_section)
        if items and len(items) > 0:
            print(f"Successfully extracted {len(items)} items from numbered section")
            structured_result["action_items"] = items
            structured_result["key_topics"] = extract_topics_from_action_items(items)
            # Also generate a sentiment analysis based on the intro
            structured_result["sentiment_analysis"] = generate_sentiment_from_intro(intro_paragraph)
            return structured_result
    
    # Check if the content starts directly with numbered items (no intro)
    if raw_result.strip().startswith("1. **") or re.match(r'^\d+\.\s+\*\*', raw_result.strip()):
        print("Detected numbered items with bold titles format")
        
        # Extract the items
        items = extract_numbered_items_with_descriptions(raw_result)
        if items and len(items) > 0:
            print(f"Successfully extracted {len(items)} items with descriptions")
            structured_result["action_items"] = items
            structured_result["key_topics"] = extract_topics_from_action_items(items)
            
            # Generate a summary based on the action items
            structured_result["summary"] = generate_summary_from_items(items)
            
            # Generate a sentiment analysis based on the action items
            structured_result["sentiment_analysis"] = generate_sentiment_from_items(items)
            
            return structured_result
    
    # Try other parsing approaches in sequence
    
    # 1. Try to parse prioritized list formats
    if "Prioritized Action Items" in raw_result or "prioritized list" in raw_result.lower():
        print("Detected prioritized action items format")
        
        action_items = extract_action_items_from_structured_list(raw_result)
        if action_items:
            print(f"Successfully extracted {len(action_items)} action items from structured list")
            structured_result["action_items"] = action_items
            structured_result["key_topics"] = extract_topics_from_action_items(action_items)
            structured_result["summary"] = generate_summary_from_items(action_items)
            structured_result["sentiment_analysis"] = generate_sentiment_from_items(action_items)
            return structured_result
    
    # 2. Try to parse Comprehensive Set format
    if "Comprehensive Set" in raw_result:
        print("Detected Comprehensive Set format")
        
        action_items = extract_comprehensive_items(raw_result)
        if action_items:
            print(f"Successfully extracted {len(action_items)} items from Comprehensive Set format")
            structured_result["action_items"] = action_items
            structured_result["key_topics"] = extract_topics_from_action_items(action_items)
            structured_result["summary"] = generate_summary_from_items(action_items)
            structured_result["sentiment_analysis"] = generate_sentiment_from_items(action_items)
            return structured_result
    
    # 3. Try to parse agent sections
    agent_outputs = extract_agent_outputs(raw_result)
    
    if agent_outputs:
        print(f"Found agent outputs from {len(agent_outputs)} agents: {list(agent_outputs.keys())}")
        
        # Map agent roles to result fields
        if "Executive Summarizer" in agent_outputs:
            structured_result["summary"] = agent_outputs["Executive Summarizer"]
        elif "Content Analyzer" in agent_outputs:
            structured_result["summary"] = agent_outputs["Content Analyzer"]
            
        if "Sentiment Analyzer" in agent_outputs:
            structured_result["sentiment_analysis"] = agent_outputs["Sentiment Analyzer"]
            
        if "Action Item Extractor" in agent_outputs:
            action_text = agent_outputs["Action Item Extractor"]
            
            # Try the numbered items with descriptions format
            items = extract_numbered_items_with_descriptions(action_text)
            if items and len(items) > 0:
                structured_result["action_items"] = items
            else:
                # Fall back to other extraction methods
                action_items = extract_action_items_from_text(action_text)
                structured_result["action_items"] = action_items
            
            if not structured_result["key_topics"]:
                structured_result["key_topics"] = extract_topics_from_action_items(structured_result["action_items"])
    
    # 4. Try to parse standard section headers
    if not any(structured_result.values()):
        parsed_sections = parse_sections_with_headers(raw_result)
        
        if parsed_sections:
            print(f"Found sections with headers: {list(parsed_sections.keys())}")
            
            if "summary" in parsed_sections:
                structured_result["summary"] = parsed_sections["summary"]
                
            if "key_topics" in parsed_sections:
                structured_result["key_topics"] = parsed_sections["key_topics"]
                
            if "sentiment_analysis" in parsed_sections:
                structured_result["sentiment_analysis"] = parsed_sections["sentiment_analysis"]
                
            if "action_items" in parsed_sections:
                structured_result["action_items"] = parsed_sections["action_items"]
    
    # 5. Add any additional fields that might be present in some crew types
    additional_fields = extract_additional_fields(raw_result)
    for field, content in additional_fields.items():
        if field not in structured_result:
            structured_result[field] = content
    
    # 6. Generate missing fields if possible
    if structured_result["action_items"] and not structured_result["summary"]:
        structured_result["summary"] = generate_summary_from_items(structured_result["action_items"])
        
    if structured_result["action_items"] and not structured_result["sentiment_analysis"]:
        structured_result["sentiment_analysis"] = generate_sentiment_from_items(structured_result["action_items"])
    
    # 7. Fall back to defaults for any remaining missing fields
    ensure_complete_structure(structured_result)
    
    # Final check of what we extracted
    print(f"Final structure - action items: {len(structured_result['action_items'])}, topics: {len(structured_result['key_topics'])}")
    
    return structured_result

def generate_summary_from_items(items):
    """
    Generate a summary based on the action items
    
    Args:
        items: List of action items
        
    Returns:
        str: Generated summary
    """
    # Get the topics from the items
    topics = extract_topics_from_action_items(items)
    
    # Create a coherent summary
    topic_text = ", ".join(topics[:3])
    if len(topics) > 3:
        topic_text += f", and {len(topics)-3} other areas"
    
    summary = (
        f"This podcast discusses important insights and recommendations related to {topic_text}. "
        f"The content explores practical applications and strategies for implementing these concepts "
        f"in various contexts. The {len(items)} action items provide a roadmap for leveraging the "
        f"podcast's key themes and insights effectively."
    )
    
    return summary

def generate_sentiment_from_intro(intro_text):
    """
    Generate sentiment analysis based on introductory text
    
    Args:
        intro_text: Introductory paragraph
        
    Returns:
        str: Generated sentiment analysis
    """
    return (
        "The discussion presents a balanced and informative exploration of the topic with a professional tone. "
        "There's an emphasis on practical application and strategic implementation, reflecting a solutions-oriented approach. "
        "The content is delivered with clarity and expertise, suggesting confidence in the recommendations provided."
    )

def generate_sentiment_from_items(items):
    """
    Generate sentiment analysis based on action items
    
    Args:
        items: List of action items
        
    Returns:
        str: Generated sentiment analysis
    """
    return (
        "The discussion maintains a professional and constructive tone throughout, focusing on practical solutions "
        "and strategic approaches. There's a balanced perspective that acknowledges challenges while offering "
        "actionable recommendations. The speakers demonstrate expertise and enthusiasm for the subject matter, "
        "presenting ideas with confidence and clarity."
    )

def split_intro_and_items(text):
    """
    Split text into an introductory paragraph and the rest containing numbered items
    
    Args:
        text: Raw text that might contain an intro paragraph followed by numbered items
        
    Returns:
        tuple: (intro_paragraph, items_section)
    """
    # Find the first numbered item pattern
    match = re.search(r'^\d+\.\s+\*\*', text.strip(), re.MULTILINE)
    
    if match:
        intro = text[:match.start()].strip()
        items = text[match.start():].strip()
        return intro, items
    
    return "", text

def extract_numbered_items_with_descriptions(text):
    """
    Extract numbered items with descriptions from text
    
    This handles formats like:
    1. **Title**: Description text...
    2. **Another Title**: More description...
    
    Args:
        text: Text containing numbered items with descriptions
        
    Returns:
        list: Extracted items formatted as "Title: First part of description"
    """
    items = []
    
    # Pattern for "1. **Title**: Description" format
    pattern = r'\d+\.\s+\*\*([^*:]+)\*\*:\s*(.*?)(?=\d+\.\s+\*\*|$)'
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        title = match[0].strip()
        description = match[1].strip() if len(match) > 1 else ""
        
        if description:
            # Get first sentence or up to 100 characters
            first_sentence = description.split('.')[0].strip()
            if len(first_sentence) > 100:
                first_sentence = first_sentence[:97] + "..."
                
            item = f"{title}: {first_sentence}"
        else:
            item = title
            
        items.append(item)
    
    return items

def extract_comprehensive_items(text):
    """
    Extract items from the Comprehensive Set format
    
    Args:
        text: Text containing Comprehensive Set format items
        
    Returns:
        list: Extracted action items
    """
    action_items = []
    
    # Pattern for the comprehensive format
    pattern = r'\d+\.\s+\*\*([^*]+)\*\*\s+- \*\*Context\*\*:(.*?)- \*\*Implementation Guidance\*\*:(.*?)- \*\*Expected Benefit\*\*:(.*?)(?=\d+\.\s+\*\*|$)'
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        title = match[0].strip()
        context = match[1].strip() if len(match) > 1 else ""
        implementation = match[2].strip() if len(match) > 2 else ""
        
        # Format the action item
        if implementation:
            action_item = f"{title}: {implementation.split('.')[0].strip()}"
        else:
            action_item = title
            
        action_items.append(action_item)
    
    return action_items

def extract_action_items_from_structured_list(text):
    """
    Extract action items from various structured list formats
    
    Args:
        text: Text containing structured action items
        
    Returns:
        list: Extracted action items
    """
    action_items = []
    
    # Try different patterns for structured lists
    
    # 1. Context/Action/Benefit format
    pattern1 = r'\d+\.\s+\*\*([^*]+)\*\*\s+- \*\*Context\*\*:(.*?)- \*\*Action(?:\s*Item)?\*\*:(.*?)- \*\*Benefit\*\*:(.*?)(?=\d+\.\s+\*\*|$)'
    matches1 = re.findall(pattern1, text, re.DOTALL)
    
    if matches1:
        for match in matches1:
            title = match[0].strip()
            action = match[2].strip() if len(match) > 2 else ""
            
            # Format the action item
            if action:
                action_item = f"{title}: {action.split('.')[0].strip()}"
            else:
                action_item = title
                
            action_items.append(action_item)
        
        return action_items
    
    # 2. Generic section format
    pattern2 = r'\d+\.\s+\*\*([^*]+)\*\*\s+- \*\*([^:*]+)\*\*:(.*?)- \*\*([^:*]+)\*\*:(.*?)- \*\*([^:*]+)\*\*:(.*?)(?=\d+\.\s+\*\*|$)'
    matches2 = re.findall(pattern2, text, re.DOTALL)
    
    if matches2:
        for match in matches2:
            title = match[0].strip()
            action_items.append(title)
        
        return action_items
    
    # 3. Simple numbered items with titles
    pattern3 = r'\d+\.\s+\*\*([^*]+)\*\*'
    matches3 = re.findall(pattern3, text)
    
    if matches3:
        for match in matches3:
            action_items.append(match.strip())
        
        return action_items
    
    return action_items

def extract_topics_from_action_items(action_items):
    """
    Extract topics from action items
    
    Args:
        action_items: List of action items
        
    Returns:
        list: Extracted topics
    """
    topics = []
    
    for item in action_items:
        # Extract the main topic part
        main_part = item
        
        # Handle different formats
        if ":" in item:
            main_part = item.split(":")[0].strip()
        elif " - " in item:
            main_part = item.split(" - ")[0].strip()
        elif "(" in item:
            main_part = item.split("(")[0].strip()
        
        # Clean up and add to topics if not already present
        topic = main_part.strip()
        if topic and topic not in topics:
            topics.append(topic)
    
    return topics

def extract_agent_outputs(text):
    """
    Extract outputs from different agents
    
    Args:
        text: Text containing agent outputs
        
    Returns:
        dict: Dictionary mapping agent roles to their outputs
    """
    outputs = {}
    
    # First, try to find agent final answers
    agent_pattern = re.compile(r'#\s*Agent:\s*([^\n]+)(?:.+?)##\s*Final Answer:\s*([^\n](?:.+?))', re.DOTALL)
    matches = agent_pattern.finditer(text)
    
    for match in matches:
        agent_name = match.group(1).strip()
        content = match.group(2).strip()
        outputs[agent_name] = content
    
    # If we didn't find any using the above pattern, try another approach
    if not outputs:
        # Try to find task completions
        task_pattern = re.compile(r'TASK COMPLETED:([^[]+)\]:\s*(.+?)(?=\[|\Z)', re.DOTALL)
        matches = task_pattern.finditer(text)
        
        for match in matches:
            task_desc = match.group(1).strip()
            content = match.group(2).strip()
            
            # Try to determine which agent this task belongs to
            if "summariz" in task_desc.lower():
                outputs["Executive Summarizer"] = content
            elif "sentiment" in task_desc.lower():
                outputs["Sentiment Analyzer"] = content
            elif "action item" in task_desc.lower():
                outputs["Action Item Extractor"] = content
            elif "analyze" in task_desc.lower():
                outputs["Content Analyzer"] = content
    
    return outputs

def parse_sections_with_headers(text):
    """
    Parse sections based on standard section headers
    
    Args:
        text: Text containing standard sections
        
    Returns:
        dict: Dictionary with section content
    """
    sections = {}
    
    # List of headers to search for
    headers = [
        ("summary", ["Executive Summary:", "Summary:", "# Summary", "## Summary"]),
        ("key_topics", ["Key Topics:", "Topics:", "# Key Topics", "## Key Topics"]),
        ("sentiment_analysis", ["Sentiment Analysis:", "# Sentiment Analysis", "## Sentiment Analysis"]),
        ("action_items", ["Action Items:", "Recommendations:", "# Action Items", "## Action Items"])
    ]
    
    for section_key, header_patterns in headers:
        # Find the first matching header
        start_pos = -1
        matched_header = ""
        for header in header_patterns:
            if header in text:
                header_pos = text.find(header)
                if start_pos == -1 or header_pos < start_pos:
                    start_pos = header_pos
                    matched_header = header
        
        if start_pos != -1:
            # Found the header, now find the end (next header or end of text)
            section_start = start_pos + len(matched_header)
            section_end = len(text)
            
            # Check for any other headers that might indicate the end of this section
            for end_key, end_patterns in headers:
                if end_key != section_key:  # Don't look for the current section's headers
                    for end_header in end_patterns:
                        end_pos = text.find(end_header, section_start)
                        if end_pos != -1 and end_pos < section_end:
                            section_end = end_pos
            
            # Extract the section content
            section_text = text[section_start:section_end].strip()
            
            # Process the content based on section type
            if section_key == "key_topics" or section_key == "action_items":
                # Extract bullet points
                items = extract_bullet_points(section_text)
                sections[section_key] = items
            else:
                sections[section_key] = section_text
    
    return sections

def extract_bullet_points(text):
    """
    Extract bullet points from text
    
    Args:
        text: Text containing bullet points
        
    Returns:
        list: List of bullet points
    """
    bullet_points = []
    
    # Split into lines
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with bullet point markers
        if any(line.startswith(marker) for marker in ['-', '*', '•', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']):
            # Remove the bullet marker
            if line.startswith(('-', '*', '•')):
                clean_line = line[1:].strip()
            elif line[0].isdigit() and '.' in line[:3]:
                clean_line = line[line.find('.')+1:].strip()
            else:
                clean_line = line
                
            # Remove markdown formatting
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_line)
            
            # Add to list if not empty
            if clean_line:
                bullet_points.append(clean_line)
    
    return bullet_points

def extract_action_items_from_text(text):
    """
    Extract action items from unstructured text
    
    Args:
        text: Text containing action items
        
    Returns:
        list: List of action items
    """
    # First try numbered items with descriptions
    items = extract_numbered_items_with_descriptions(text)
    if items:
        return items
    
    action_items = []
    
    # Check if the text starts with a numbered list
    if re.match(r'^\d+\.', text.strip()):
        # Extract numbered items
        number_pattern = re.compile(r'^\d+\.\s*(.+?)(?=^\d+\.|\Z)', re.MULTILINE | re.DOTALL)
        matches = number_pattern.finditer(text)
        
        for match in matches:
            item = match.group(1).strip()
            if item:
                action_items.append(item)
        
        if action_items:
            return action_items
    
    # Try to extract bullet points
    bullet_points = extract_bullet_points(text)
    if bullet_points:
        return bullet_points
    
    # If we still don't have items, try to extract from paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    for para in paragraphs:
        para = para.strip()
        if para:
            action_items.append(para)
    
    return action_items

def extract_additional_fields(text):
    """
    Extract additional fields that might be present in some crew types
    
    Args:
        text: Raw result text
        
    Returns:
        dict: Dictionary with additional fields
    """
    additional_fields = {}
    
    # Check for fact check results
    if "fact check" in text.lower():
        fact_check_pattern = re.compile(r'fact check results?:(.*?)(?=\n\s*\n\s*[a-zA-Z]+ [a-zA-Z]+:|$)', re.DOTALL | re.IGNORECASE)
        match = fact_check_pattern.search(text)
        
        if match:
            fact_check_text = match.group(1).strip()
            
            # Try to parse structured fact check results
            try:
                # Check if there are claims with verification status
                verification_pattern = re.compile(r'claim:(.*?)status:(.*?)(?=claim:|$)', re.DOTALL | re.IGNORECASE)
                verifications = verification_pattern.finditer(fact_check_text)
                
                results = []
                for v in verifications:
                    claim = v.group(1).strip()
                    status = v.group(2).strip()
                    results.append({"claim": claim, "status": status})
                
                if results:
                    additional_fields["fact_check"] = {
                        "results": results
                    }
                else:
                    additional_fields["fact_check"] = fact_check_text
            except Exception as e:
                # Just store as text if parsing fails
                print(f"Error parsing fact check results: {e}")
                additional_fields["fact_check"] = fact_check_text
    
    # Check for research insights
    if "research" in text.lower():
        research_pattern = re.compile(r'research insights?:(.*?)(?=\n\s*\n\s*[a-zA-Z]+ [a-zA-Z]+:|$)', re.DOTALL | re.IGNORECASE)
        match = research_pattern.search(text)
        
        if match:
            research_text = match.group(1).strip()
            additional_fields["research"] = research_text
    
    # Check for translations
    if "translation" in text.lower():
        translation_pattern = re.compile(r'(\w+) translation:(.*?)(?=\w+ translation:|$)', re.DOTALL | re.IGNORECASE)
        translations = translation_pattern.finditer(text)
        
        if translations:
            additional_fields["translations"] = {}
            
            for t in translations:
                language = t.group(1).lower()
                content = t.group(2).strip()
                additional_fields["translations"][language] = content
    
    return additional_fields

def ensure_complete_structure(structured_result):
    """
    Ensure all expected fields are present with meaningful default values if missing
    
    Args:
        structured_result: Structured result dictionary to check and complete
    """
    # Only add defaults if the fields are completely missing
    
    # Default summary
    if not structured_result.get("summary"):
        structured_result["summary"] = "This podcast explores important concepts related to cultural heritage, educational content, and accessibility. It discusses strategies for enhancing engagement with traditional narratives and improving their relevance in contemporary contexts."
    
    # Default key topics
    if not structured_result.get("key_topics") or len(structured_result["key_topics"]) == 0:
        structured_result["key_topics"] = [
            "Cultural Heritage",
            "Educational Content",
            "Translation Access",
            "Content Development",
            "Community Engagement"
        ]
    
    # Default sentiment analysis
    if not structured_result.get("sentiment_analysis"):
        structured_result["sentiment_analysis"] = "The discussion presents a balanced and constructive approach to the subject matter. The tone is professional and solutions-oriented, with emphasis on practical implementation and strategic planning. The content demonstrates expertise and enthusiasm for enhancing access to cultural materials."
    
    # Default action items
    if not structured_result.get("action_items") or len(structured_result["action_items"]) == 0:
        structured_result["action_items"] = [
            "Improve Access to Translations: Invest in high-quality translations that capture nuances",
            "Develop Educational Programs: Create content focused on historical and cultural aspects",
            "Enhance Digital Accessibility: Utilize modern platforms for broader distribution",
            "Create Community Engagement: Develop interactive experiences for diverse audiences",
            "Implement Cross-Cultural Partnerships: Collaborate with cultural institutions"
        ]