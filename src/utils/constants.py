AGREE_PHRASES = [
    "accept",
    "consent",
    "approve",
    "affirm",
    "acknowledge",
    "concur",
    "settle",
    "come to terms",
    "reach an understanding",
    "see eye to eye",
    "be on the same page",
    "align",
    "share the same view",
    "be of the same mind",
    "hold the same opinion",
    "support",
    "sanction",
    "ratify",
    "endorse",
    "authorize",
    "I totally agree",
    "I completely agree",
    "I couldn't agree more",
    "Absolutely!",
    "Exactly!",
    "That's so true",
    "You're absolutely right",
    "I'm with you on that",
    "No doubt about it",
    "That's exactly how I feel",
    "You nailed it",
    "I feel the same way",
    "That's a good point",
    "We're on the same page",
    "I second that",
    "I’m all for it",
    "Preach!",
    "100% agree",
    "Totally!",
    "Couldn't have said it better myself"
]


FUNCTION_MAPPING_NAME = {
    '/winlost_detail': 'Win Loss Report',
    '/betcount': 'Bet Count Report', 
    '/turnover': 'Turnover Report',
    '/outstanding': 'Outstanding Report',
    '/topoutstanding': 'Top Outstanding Report',
    '/net_turnover': 'Net Turnover Report',
    '/gross_comm': 'Gross Commission Report',
    '/member': 'Member Report',
    '/agent': 'Agent Report',
    '/master': 'Master Report',
    '/super': 'Super Report',
    '/company': 'Company Report',
    '/reward': 'Reward Report',
    None: 'Could not find the Function/Report, please give me a valid Function/Report'
}

DEPARTMENT_MAPPING_NAME = [
    'Alpha'
] 

WEIGHT_VOTING_SEARCH = {
    "semantic_search": 0.9,
    "keyword_search": 0.1
}

WEIGHT_VOTING_REPORT = {
    "report_calling_agent": 0.5,
    "abbreviation_recognizer_agent": 0.5
}

WEIGHT_VOTING_ENTITY = {
    "abbreviation_recognizer_agent": 0.5,
    "ner_agent": 0.5
}

ICONS = {
    "from_date": "📅",
    "to_date": "📅",
    "product": "🏢",
    "product_detail": "📋",
    "level": "🎮",
    "user": "👤",
    "top": "🔝"
}