import jieba.analyse
import pymongo
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import csv

MONGO_URI = '127.0.0.1:27017'
MONGO_DATABASE = 'position'
collection_name = 'PositionItem'

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

# Handling salary field
# for position in db[collection_name].find():
#     db[collection_name].update_one({'positionId': position['positionId']},
#                                    {'$set': {'salary': re.match('\d+', position['salary']).group(0) + 'K'}})

text = ''
for position in db[collection_name].find():
    text += position['description'] + '\n'
jieba.analyse.set_stop_words('stop_words.txt')
tags = jieba.analyse.extract_tags(text, 100, withWeight=True, allowPOS=('n', 'eng'))
wordcloud = WordCloud(font_path='C:\Windows\Fonts\Microsoft YaHei\msyh.ttc').fit_words(dict(tags))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
# mongoexport --db position --collection PositionItem --type=csv --fields positionId,education,city,salary,workYear,companySize,financeStage --out PositionItem.csv

# Handling and exporting industryField field
# industryField_list = {}
# for position in db[collection_name].find():
#     if position['industryField'] is not None:
#         for industryFields in position['industryField'].split(','):
#             for industryField in industryFields.split('、'):
#                 industryField_list[industryField] = industryField_list.get(industryField, 1) + 1
# with open('IndustryField.csv', 'w', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['industryField', 'totalCount'])
#     writer.writerows(industryField_list.items())
