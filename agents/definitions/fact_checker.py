# agents/definitions/fact_checker.py
from agents.base import BaseAgent
from agents.registry import register_agent
from api.wiki_api import search_wikipedia

@register_agent("fact_checker")
class FactCheckerAgent(BaseAgent):
    """Agent specialized in checking factual accuracy of Meeting content"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Fact Checker Agent"""
        super().__init__(
            role="Fact Checker",
            goal="Identify and verify factual claims made in the Meeting",
            backstory="I'm a seasoned fact-checker with experience working for major news organizations. "
                    "I have a meticulous attention to detail and can quickly identify factual claims "
                    "that require verification. I use multiple reliable sources to confirm "
                    "information and present findings in a clear, unbiased manner.",
            model=model
        )
    
    def extract_claims(self, transcript_content):
        """
        Extract factual claims from a transcript
        
        Args:
            transcript_content: Processed transcript content
            
        Returns:
            list: List of extracted claims
        """
        from agents.tasks.fact_checking import FactCheckingTask
        
        # Create and execute a claim extraction task
        task = FactCheckingTask.create_claim_extraction_task(self, transcript_content)
        result = self.execute_task(task)
        
        # Parse the result to get a list of claims
        # This assumes the result is a formatted string with claims
        claims = []
        for line in result.strip().split('\n'):
            if line.strip().startswith('- ') or line.strip().startswith('* ') or ': ' in line:
                claims.append(line.strip())
        
        return claims
    
    def verify_claim(self, claim, use_wikipedia=True):
        """
        Verify a single factual claim
        
        Args:
            claim: The claim to verify
            use_wikipedia: Whether to use Wikipedia API for verification
            
        Returns:
            dict: Verification result
        """
        verification_context = ""
        
        # If enabled, use Wikipedia API to get additional context
        if use_wikipedia:
            try:
                # Extract key terms from the claim
                search_query = " ".join(claim.split()[:5])  # Use first 5 words as search
                wiki_results = search_wikipedia(search_query)
                
                if wiki_results:
                    verification_context = f"Wikipedia context: {wiki_results[:1000]}"
            except Exception as e:
                print(f"Error accessing Wikipedia API: {e}")
        
        # Create a verification task
        from agents.tasks.fact_checking import FactCheckingTask
        input_data = {
            "claim": claim,
            "context": verification_context
        }
        
        task = FactCheckingTask.create_verification_task(self, input_data)
        verification_result = self.execute_task(task)
        
        # Convert the result string to a structured dictionary
        # This assumes a specific format in the response
        status = "Unknown"
        if "TRUE" in verification_result.upper() or "VERIFIED" in verification_result.upper():
            status = "Verified"
        elif "FALSE" in verification_result.upper() or "INCORRECT" in verification_result.upper():
            status = "Refuted"
        elif "PARTIALLY" in verification_result.upper():
            status = "Partially Verified"
        elif "UNVERIFIABLE" in verification_result.upper() or "INSUFFICIENT" in verification_result.upper():
            status = "Unverifiable"
        
        result = {
            "claim": claim,
            "status": status,
            "details": verification_result,
            "sources": []  # Add sources from verification result if available
        }
        
        return result
    
    def check_transcript_facts(self, transcript_content, max_claims=10):
        """
        Check facts in a transcript
        
        Args:
            transcript_content: Processed transcript content
            max_claims: Maximum number of claims to check
            
        Returns:
            dict: Fact checking results
        """
        # Extract claims from the transcript
        claims = self.extract_claims(transcript_content)
        
        # Limit the number of claims to check
        if len(claims) > max_claims:
            claims = claims[:max_claims]
        
        # Verify each claim
        verification_results = []
        for claim in claims:
            result = self.verify_claim(claim)
            verification_results.append(result)
        
        # Prepare the final report
        report = {
            "total_claims": len(claims),
            "verified_claims": sum(1 for r in verification_results if r["status"] == "Verified"),
            "refuted_claims": sum(1 for r in verification_results if r["status"] == "Refuted"),
            "uncertain_claims": sum(1 for r in verification_results if r["status"] not in ["Verified", "Refuted"]),
            "results": verification_results
        }
        
        return report