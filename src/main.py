import streamlit as st
import pandas as pd
import networkx as nx
import numpy as np
from PIL import Image

def main():
    st.header('Network analyst Game of Thorne')
    MENU = ['Home', 'Data Analyst', 'Build Network']
    choice = st.sidebar.selectbox('Navigation', MENU)
    if choice == MENU[0]:
        home()
    if choice == MENU[1]:
        DA()
    if choice == MENU[2]:
        NB()



def home():
    image = Image.open('src/data/intro.jpg')
    st.image(image, caption='Network analyst Game of throne', use_column_width=True)


def DA():
    st.header('I - Data Analyst')
    st.markdown('**1. Kiểm tra edges**')
    edgesBook1 = pd.read_csv('src/data/asoiaf-book1-edges.csv')
    edgesBook1.drop(['Type', 'book'],axis=1, inplace=True)
    st.dataframe(edgesBook1)
    r, c = edgesBook1.shape
    st.write(' - Số lượng edge: ', r)

    st.markdown('**2. Kiểm tra Duplicate edges**')
    with st.echo():
        countDuplicates = edgesBook1.duplicated().sum()
    st.write('- Số lượng duplicate rows trong DataFrame: ', countDuplicates)
    st.write('=> Không có DUPLICATE. Tiếp tục kiểm tra có bao nhiêu Nodes có trong mạng')

    st.markdown('_**3. Kiểm tra Nodes**_')
    sourceNode = edgesBook1['Source']
    sourceNode = sourceNode.rename({'Source': 'Node'})
    targetNode = edgesBook1['Target']
    targetNode = targetNode.rename({'Target': 'Node'})
    checkingNode = sourceNode.append(targetNode)
    checkingNode = checkingNode.drop_duplicates()
    checkingNode.reset_index(drop=True, inplace=True)
    r, = checkingNode.shape
    st.write('Số lượng Node: ', r)
    st.write('Có ', r ,' **Nodes** trong mạng. Tiếp tục kiểm tra có tồn tại **NULL VALUES**_ trong dataframe hay không ?')

    st.markdown('_**4. Kiểm tra null values**_')
    with st.echo():
        pd.isnull(edgesBook1).sum() > 0
    st.write('=> Không có NULL VALUES trong dataframe')

def NB():
    st.header('II - Build Network')

    edgesBook1 = pd.read_csv('src/data/asoiaf-book1-edges.csv')
    edgesBook1.drop(['Type', 'book'],axis=1, inplace=True)
    sourceNode = edgesBook1['Source']
    sourceNode = sourceNode.rename({'Source': 'Node'})
    targetNode = edgesBook1['Target']
    targetNode = targetNode.rename({'Target': 'Node'})
    checkingNode = sourceNode.append(targetNode)
    checkingNode = checkingNode.drop_duplicates()
    checkingNode.reset_index(drop=True, inplace=True)

    Graph = nx.Graph()
    for _, edge in edgesBook1.iterrows():
        Graph.add_edge(edge['Source'], edge['Target'], weight=edge['weight'])
    
    st.markdown('_**1. Centrality measures**_')
    st.write('- Degree Centrality')
    st.write('- Closeness Centrality')
    
    st.markdown('> _**1.2. Degree Centrality**_')
    degreeCentrality= nx.degree_centrality(Graph)
    dfDegreeCentrality = pd.DataFrame(list(degreeCentrality.items()),columns = ['Character','Degree Centrality'])
    dfDegreeCentrality.sort_values("Degree Centrality", axis = 0, ascending = False, inplace = True)
    st.dataframe(dfDegreeCentrality)

    st.markdown('> _**1.3. Closeness Centrality**_')
    closenessCentrality= nx.closeness_centrality(Graph)
    dfClosenessCentrality = pd.DataFrame(list(closenessCentrality.items()),columns = ['Character','Closeness Centrality'])
    dfClosenessCentrality.sort_values("Closeness Centrality", axis = 0, ascending = False, inplace = True) 
    st.dataframe(dfClosenessCentrality)

    st.markdown('_**2. Spectral measures**_')
    st.write('- Page rank')
    st.write('- Eigenvector Centrality')

    st.markdown('> _**2.1. Page rank**_')
    pageRank =nx.pagerank(Graph, tol=0.001)
    dfPageRank = pd.DataFrame(list(pageRank.items()),columns = ['Character','Page Rank'])
    dfPageRank.sort_values("Page Rank", axis = 0, ascending = False, inplace = True) 
    st.dataframe(dfPageRank)

    st.markdown('> _**2.2. Eigenvector Centrality**_')
    eigenCen = nx.eigenvector_centrality(Graph)
    dfEigenCentrality = pd.DataFrame(list(eigenCen.items()),columns = ['Character','Eigenvector Centrality'])
    dfEigenCentrality.sort_values("Eigenvector Centrality", axis = 0, ascending = False, inplace = True)
    st.dataframe(dfEigenCentrality)

    st.markdown('_**3. Path Based measures**_')
    st.write('- Betweeness Centrality')
    betweenCen = nx.betweenness_centrality(Graph)
    dfBetweenCentrality = pd.DataFrame(list(betweenCen.items()),columns = ['Character','Betweenness Centrality'])
    dfBetweenCentrality.sort_values("Betweenness Centrality", axis = 0, ascending = False, inplace = True) 
    st.dataframe(dfBetweenCentrality)

    sum = pd.DataFrame((dfDegreeCentrality['Character'].values,
        dfClosenessCentrality['Character'].values,
        dfPageRank['Character'].values,
        dfEigenCentrality['Character'].values,
        dfBetweenCentrality['Character'].values),
        index=['Degree Centrality', 'Closeness Centrality', 'Pagerank', 'Eigenvector Centrality', 'Betweenness Centrality']).transpose()

    st.header('Summary _**Network Cetrality**_')
    st.dataframe(sum)

def graph_to_edge_matrix(G):
    edgeMat = np.zeros((len(G), len(G)), dtype=int)
    for node in G:
        for neighbor in G.neighbors(node):
            edgeMat[node][neighbor] = 1
        edgeMat[node][node] = 1
    return edgeMat

if __name__ == '__main__':
    main()
