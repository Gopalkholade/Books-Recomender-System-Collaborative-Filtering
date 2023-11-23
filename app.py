from flask import Flask, render_template,request
import pickle as pkl
import numpy as np


popular_df = pkl.load(open("./resourses/popular.pkl",'rb'))
pt = pkl.load(open("./resourses/pt.pkl",'rb'))
books = pkl.load(open("./resourses/books.pkl",'rb'))
similarity_score = pkl.load(open("./resourses/similarity_score.pkl",'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_rating'].values),
                           rating = list(popular_df['avg_rating'].round(2,).values))


@app.route('/recommender')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods = ['post'])
def recommend_books():
    user_input = request.form.get('user_input')

    index = np.where(pt.index==user_input)[0][0]
    simillar_items = sorted(list(enumerate(similarity_score[index])),key= lambda x: x[1],reverse=True)[1:6]
    # suggestion = [pt.index[i[0]] for i in simillar_items]    
    data = []
    for i in simillar_items:
        item = []
        temp_df = books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html',data=data)
if __name__ == "__main__":
    app.run(debug=True)

