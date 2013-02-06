import re
from topia.termextract import extract

extractor = extract.TermExtractor()
extractor.filter=extract.permissiveFilter
msgbody = "Homeo hospital near to anby plaza"
msgbody = re.sub(r'[^\w]', ' ', msgbody)
list = extractor(msgbody)
print list
