
class NerAgentImpl(NerAgent):
    """
    Implementation of NerAgent using Ollama API for Named Entity Recognition.
    """
    
    def __init__(
        self,
        llm: LLM
    ) -> None:
        """
        Initialize the NerAgentImpl with Ollama API configuration.
        
        Args:
            url (str): The Ollama API endpoint URL
            model (str): The model name to use for NER
        """
        self.llm = llm
        self.system_prompt = "You are an AI assistant majoring for Named Entity Recognition trained to extract entity and categorize queries for Winlost Report Detail"
        self.format = {
            "type": "object",
            "properties": {
                "date_range": {"type": "string"},
                "from_date": {"type": "string"},
                "to_date": {"type": "string"},
                "product": {"type": "string"},
                "product_detail": {"type": "string"},
                "level": {"type": "string"},
                "user": {"type": "string"}
            },
            "required": ["date_range", "from_date", "to_date", "product", "product_detail", "level", "user"]
        }
        
        self.date_format = {
            "type": "object",
            "properties": {
                "date_range": {"type": "string"},
                "from_date": {"type": "string"},
                "to_date": {"type": "string"}
            },
            "required": ["date_range", "from_date", "to_date"]
        }
        
        self.product_format = {
            "type": "object",
            "properties": {
                "product": {"type": "string"}
            },
            "required": ["product"]
        }
        
        self.product_detail_format = {
            "type": "object",
            "properties": {
                "product_detail": {"type": "string"}
            },
            "required": ["product_detail"]
        }
        
        self.level_format = {
            "type": "object",
            "properties": {
                "level": {"type": "string"}
            },
            "required": ["level"]
        }

    def _get_date_prompt(self, text: str) -> str:
        current_date = get_current_date()
        current_year = get_current_year()   
        current_month = get_current_month()
        
        user_prompt = f"""
        Current date: {current_date}
        Current year: {current_year}
        Current month: {current_month}

        # Define your task:
        Extract date information from the following sentence: '{text}'. 
        Detect any words related to dates such as tomorrow, today, last week, next year, so on.
        Help me convert the date range to the format of YYYY-MM-DD to YYYY-MM-DD.
        
        # For date range, please help me convert it to from_date and to_date in DD/MM/YYYY format following these cases:

        1. If a single date is mentioned (e.g. "day 10"):
           - Use current month and year {current_year} and {current_month}
           - Set both from_date and to_date to that date
           Example: "day 10" -> from_date: 10/{current_month}/{current_year}, to_date: 10/{current_month}/{current_year}

        2. If a date range is specified (e.g. "01/02/2024 to 15/02/2024"):
            - Note that in this case, the date range derived from user's query must be DD/MM/YYYY format
            - Keep the dates as specified in DD/MM/YYYY format
           Example: "01/02/2024 to 15/02/2024" -> from_date: 01/02/2024, to_date: 15/02/2024

        3. If relative dates are mentioned:
           - "today" -> Use {current_date} for both
           - "yesterday" -> Use yesterday's date for both from current date {current_date}
           - "last week" -> from_date is 7 days ago, to_date is today from current date {current_date}
           - "last month" -> from_date is 1st of previous month, to_date is last day of previous month from current date {current_date}
           - "last year" -> from_date is Jan 1st of previous year, to_date is Dec 31st of previous year from current date {current_date}
           - "this week" -> from_date is Monday of current week, to_date is today from current date {current_date}
           - "this month" -> from_date is 1st of current month, to_date is today from current date {current_date}
           - "this year" -> from_date is Jan 1st of current year, to_date is today from current date {current_date}
           
        4. If a month range is specified (e.g. "1/1 to 31/1"):
           - Use current year {current_year}
           - Set from_date to first day of specified month 
           - Set to_date to last day of specified month
           Example: "1/1 to 31/1" in {current_year} -> from_date: 01/01/{current_year}, to_date: 31/01/{current_year}
           
        5. If no date is specified:
           - Set date_range as "N/A"
           - Set both from_date and to_date as "N/A"
           
        # Example 1:
        ## User: Get me a Win Loss Detail Report on day 10
        ## Output:
        {{
            "date_range": "day 10",
            "from_date": "10/{current_month}/{current_year}",
            "to_date": "10/{current_month}/{current_year}"
        }}
        
        # Example 2:
        ## User: Get me a Win Loss Detail Report from 01/02/2024 to 15/02/2024
        ## Output:
        {{
            "date_range": "01/02/2024 to 15/02/2024",
            "from_date": "01/02/2024",
            "to_date": "15/02/2024"
        }}
        
        # Example 3:
        ## User: Win/Loss details for Product Sportsbook
        ## Output:
        {{
            "date_range": "N/A",
            "from_date": "N/A",
            "to_date": "N/A"
        }}
        """
        return user_prompt
    
    def _get_product_prompt(self, text: str) -> str:
        # Chuyển danh sách sản phẩm sang chữ thường để so sánh
        lowercase_products = [p.lower() for p in a.PRODUCT]
        
        user_prompt = f"""
        # Define your task:
        Extract product information from the following sentence: '{text.lower()}'.
        If no product is specified, return 'All'.
        
        Here is the list of products you should detect (PLEASE ONLY return product name that is in the list):
        ### PRODUCT = {lowercase_products}
        
        
        # Example 1:
        ## User: Get me a Win Loss Detail Report for Sportsbook
        ## Output:
        {{
            "product": "Sportsbook"
        }}
        
        # Example 2:
        ## User: Win/Loss details for SABA Basketball
        ## Output:
        {{
            "product": "SABA Basketball"
        }}
        
        # Example 3:
        ## User: Show me the report
        ## Output:
        {{
            "product": "All"
        }}
        """
        return user_prompt
    
    def _get_product_detail_prompt(self, text: str) -> str:
        # Chuyển danh sách chi tiết sản phẩm sang chữ thường để so sánh
        lowercase_product_details = [pd.lower() for pd in a.PRODUCT_DETAIL]
        
        user_prompt = f"""
        # Define your task:
        Extract product detail information from the following sentence: '{text.lower()}'.
        If no product detail is specified, return 'All'.
        
        Here is the list of product details you should detect (PLEASE ONLY return product detail name that is in the list):
        ### PRODUCT_DETAIL = {lowercase_product_details}
        
        # Example 1:
        ## User: Get me a Win Loss Detail Report for Product Detail Sportsbook
        ## Output:
        {{
            "product_detail": "Sportsbook"
        }}
        
        # Example 2:
        ## User: Win/Loss details for Product Detail SABA Basketball
        ## Output:
        {{
            "product_detail": "SABA Basketball"
        }}
        
        # Example 3:
        ## User: Show me the report
        ## Output:
        {{
            "product_detail": "All"
        }}
        """
        return user_prompt
    
    def _get_level_prompt(self, text: str) -> str:
        # Chuyển danh sách cấp độ sang chữ thường để so sánh
        lowercase_levels = [l.lower() for l in a.LEVEL]
        
        user_prompt = f"""
        # Define your task:
        Extract level information from the following sentence: '{text.lower()}'.
        If no level is specified, return 'All'.
        
        Here is the list of levels you should detect:
        ### LEVEL = {lowercase_levels}
        
        # Example 1:
        ## User: Get me a Win Loss Detail Report for Direct Member
        ## Output:
        {{
            "level": "Direct Member"
        }}
        
        # Example 2:
        ## User: Win/Loss details for Super Agent
        ## Output:
        {{
            "level": "Super Agent"
        }}
        
        # Example 3:
        ## User: Show me the report
        ## Output:
        {{
            "level": "All"
        }}
        """
        return user_prompt

    def _extract_date_info(self, text: str) -> Dict[str, Any]:
        """Extract date information from text."""
        date_prompt = self._get_date_prompt(text)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": date_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages,
            format_schema=self.date_format,
            endpoint='/api/chat'
        )
        
        result = json.loads(response) if response else {}
        
        if not result:
            return {
                "date_range": "N/A",
                "from_date": "N/A",
                "to_date": "N/A"
            }
        
        return result
    
    def _extract_product_info(self, text: str) -> Dict[str, Any]:
        """Extract product information from text."""
        product_prompt = self._get_product_prompt(text)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": product_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages,
            format_schema=self.product_format,
            endpoint='/api/chat'
        )
        
        result = json.loads(response) if response else {}
        
        if not result:
            return {"product": "All"}
            
        # Xử lý trường hợp LLM trả về nhiều sản phẩm kết hợp
        extracted_product = result.get("product", "All")
        if extracted_product != "All":
            # Tách chuỗi thành danh sách các sản phẩm có thể
            product_candidates = [p.strip() for p in extracted_product.split(',')]
            
            # Tạo một dict mapping từ lowercase sang original case
            product_case_map = {p.lower(): p for p in a.PRODUCT}
            
            # Chỉ giữ lại các sản phẩm hợp lệ, dùng lowercase để so sánh
            valid_products = []
            for p in product_candidates:
                # Vì LLM trả về lowercase, nên không cần chuyển đổi p sang lowercase nữa
                if p in product_enums:
                    # Nếu tìm thấy match, dùng phiên bản chính xác trong a.PRODUCT
                    valid_products.append(product_enums[p])
            
            if valid_products:
                # Nếu có sản phẩm hợp lệ, kết hợp chúng
                result["product"] = ", ".join(valid_products)
            else:
                # Nếu không có sản phẩm hợp lệ, trả về "All"
                result["product"] = "All"
        
        return result
    
    def _extract_product_detail_info(self, text: str) -> Dict[str, Any]:
        """Extract product detail information from text."""
        product_detail_prompt = self._get_product_detail_prompt(text)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": product_detail_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages,
            format_schema=self.product_detail_format,
            endpoint='/api/chat'
        )
        
        result = json.loads(response) if response else {}
        
        if not result:
            return {"product_detail": "All"}
            
        # Xử lý trường hợp LLM trả về nhiều chi tiết sản phẩm kết hợp
        extracted_product_detail = result.get("product_detail", "All")
        if extracted_product_detail != "All":
            # Tách chuỗi thành danh sách các chi tiết sản phẩm có thể
            product_detail_candidates = [pd.strip() for pd in extracted_product_detail.split(',')]
            
            # Tạo một dict mapping từ lowercase sang original case
            product_detail_case_map = {pd.lower(): pd for pd in a.PRODUCT_DETAIL}
            
            # Chỉ giữ lại các chi tiết sản phẩm hợp lệ, dùng lowercase để so sánh
            valid_product_details = []
            for pd in product_detail_candidates:
                # Vì LLM trả về lowercase, nên không cần chuyển đổi pd sang lowercase nữa
                if pd in product_detail_case_map:
                    # Nếu tìm thấy match, dùng phiên bản chính xác trong a.PRODUCT_DETAIL
                    valid_product_details.append(product_detail_case_map[pd])
            
            if valid_product_details:
                # Nếu có chi tiết sản phẩm hợp lệ, kết hợp chúng
                result["product_detail"] = ", ".join(valid_product_details)
            else:
                # Nếu không có chi tiết sản phẩm hợp lệ, trả về "All"
                result["product_detail"] = "All"
        
        return result
    
    def _extract_level_info(self, text: str) -> Dict[str, Any]:
        """Extract level information from text."""
        level_prompt = self._get_level_prompt(text)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": level_prompt}
        ]
        
        response = self.llm.invoke(
            messages=messages,
            format_schema=self.level_format,
            endpoint='/api/chat'
        )
        
        result = json.loads(response) if response else {}
        
        if not result:
            return {"level": "All"}
            
        # Xử lý trường hợp LLM trả về nhiều cấp độ kết hợp
        extracted_level = result.get("level", "All")
        if extracted_level != "All":
            # Tách chuỗi thành danh sách các cấp độ có thể
            level_candidates = [l.strip() for l in extracted_level.split(',')]
            
            # Tạo một dict mapping từ lowercase sang original case
            level_case_map = {l.lower(): l for l in a.LEVEL}
            
            # Chỉ giữ lại các cấp độ hợp lệ, dùng lowercase để so sánh
            valid_levels = []
            for l in level_candidates:
                # Vì LLM trả về lowercase, nên không cần chuyển đổi l sang lowercase nữa
                if l in level_case_map:
                    # Nếu tìm thấy match, dùng phiên bản chính xác trong a.LEVEL
                    valid_levels.append(level_case_map[l])
            
            if valid_levels:
                # Nếu có cấp độ hợp lệ, kết hợp chúng
                result["level"] = ", ".join(valid_levels)
            else:
                # Nếu không có cấp độ hợp lệ, trả về "All"
                result["level"] = "All"
        
        return result

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Process the input text and extract named entities using separate prompts for each entity type.
        Utilizes multithreading to process extractions in parallel.
        
        Args:
            text (str): The input text to process
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted entities and their metadata
        """
        # Sử dụng ThreadPoolExecutor để chạy các trích xuất song song
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Gửi các công việc cho executor
            date_future = executor.submit(self._extract_date_info, text)
            product_future = executor.submit(self._extract_product_info, text)
            product_detail_future = executor.submit(self._extract_product_detail_info, text)
            level_future = executor.submit(self._extract_level_info, text)
            
            # Lấy kết quả khi hoàn thành
            date_info = date_future.result()
            product_info = product_future.result()
            product_detail_info = product_detail_future.result()
            level_info = level_future.result()
        
        # Kết hợp kết quả
        result = {
            "date_range": date_info.get("date_range", "N/A"),
            "from_date": date_info.get("from_date", "N/A"),
            "to_date": date_info.get("to_date", "N/A"),
            "product": product_info.get("product", "All"),
            "product_detail": product_detail_info.get("product_detail", "All"),
            "level": level_info.get("level", "All"),
            "user": "N/A"  # Default value for user
        }
        
        return result

    def get_entity_types(self) -> List[str]:
        """
        Get the list of entity types that this NER agent can recognize.
        
        Returns:
            List[str]: List of supported entity types
        """
        return ["date_range", "from_date", "to_date", "product", "product_detail", "level", "user"]