# MovieLens 1M数据集 GroupLens Research（http://www.grouplens.org/node/73）采集了一组从20世纪90年末到21世纪初由MovieLens用户提供的电影评分数据。这些数据中包括电影评分、电影元数据（风格类型和年代）以及关于用户的人口统计学数据（年龄、邮编、性别和职业等）。基于机器学习算法的推荐系统一般都会对此类数据感兴趣。虽然我不会在本书中详细介绍机器学习技术，但我会告诉你如何对这种数据进行切片切块以满足实际需求。 416 MovieLens 1M数据集含有来自6000名用户对4000部电影的100万条评分数据。它分为三个表：评分、用户信息和电影信息。将该数据从zip文件中解压出来之后，可以通过pandas.read_table将各个表分别读到一个pandas DataFrame对象中

import pandas as pd

# Make display smaller
# pd.options.display.max_rows = 10

#先加载数据集成为dataframe
# 如果打不开，错误了，加上encoding='ISO-8859-1'
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('datadata2023/users.dat', sep='::',
header=None, names=unames,encoding='ISO-8859-1')
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('datadata2023/ratings.dat', sep='::',
header=None, names=rnames,encoding='ISO-8859-1')
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('datadata2023/movies.dat', sep='::',
header=None, names=mnames,encoding='ISO-8859-1')



# 我们先用pandas的merge函数将ratings跟users合并到一起，
# 然后再将movies也合并进去。pandas会根据列名的重叠
# 情况推断出哪些列是合并（或连接）键：
data = pd.merge(pd.merge(ratings, users), movies)
# 初步实现：
# print(data[:5])
#查看其中一则行，看看信息
# print(data.iloc[0])
# 尝试导出文档：
# data.to_csv('movie.csv')

# 为了按性别计算每部电影的平均得分，我们可以使用pivot_table方法：
# 了解pivot_table
mean_ratings = data.pivot_table(value='rating', index='title',
columns='gender', aggfunc='mean')
# 初步实现：
# print(mean_ratings[:5])
# 该操作产生了另一个DataFrame，其内容为电影平均得分，行标为电影名称（索引），列标为性别。

#打算过滤掉评分数据不够250条的电影:
# 先对title进行分组，然后利用size()得到一个含有各电影分组大小的Series对象：
ratings_by_title = data.groupby('title').size()
#初步实现：
# print(ratings_by_title[:10])
#筛选size大于250的
active_titles = ratings_by_title.index[ratings_by_title >= 250]
# print(active_titles)
#最后，用active_titles来索引,btw不能改名称啊...我不知道怎么讲
mean_ratings = mean_ratings.loc[active_titles]

#女性观众最喜欢的电影，我们可以对F列降序排列
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)

# 计算评分分歧
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']

# 按"diff"排序即可得到分歧最大的电影：
sorted_by_diff = mean_ratings.sort_values(by='diff')

print(sorted_by_diff)



