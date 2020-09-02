import json
from collections import Counter
import matplotlib.pyplot as plt
import pickle
from lxml import html
import requests
import re
import seaborn as sns
import statistics

def getLibraries(file):
    import_repo = []

    with open(file, encoding='utf-8') as f:
        for file_line in f:
            file_line = file_line.split("\n")[0]
            try:
                with open('./../Dataset/' + file_line,encoding='utf-8') as fp:
                    for code_line in fp:
                        code_line = code_line.split("\n")[0]
                        code_line = code_line.split(" ")
                        if code_line[0] == "from" or code_line[0] == "import":
                            import_repo.append(code_line[1])
            except:
                continue

    print(import_repo)



def listCount(file, stop_count):

    with open(file, 'rb') as fp:
        itemlist = pickle.load(fp)

    lib_dict = Counter(itemlist)
    sorted_dict = sorted(lib_dict.items(), key=lambda x: x[1], reverse=True)

    count=0
    len(sorted_dict)
    del sorted_dict[1]
    del sorted_dict[11]
    del sorted_dict[13]
    lib = []
    lib_count = []

    for key in sorted_dict:
        lib.append(key[0])
        lib_count.append(key[1])
        count+=1
        if count == stop_count:
            break

    print(lib)
    print(lib_count)

    plt.bar(lib, lib_count)
    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-large'
    )
    plt.show()

def getContext(file):

    topics = []
    stars = []
    url_success_count = 0
    repo_accessed_count = 0
    repo_count = 0
    with open(file) as fp:
        for line in fp:
            repo_count += 1
            line = line.split()
            try:
                page = requests.get(line[1])
                tree = html.fromstring(page.content)
                topic = tree.xpath('//a[@class="topic-tag topic-tag-link "]/text()')
                star = tree.xpath('//a[@class="social-count js-social-count"]/text()')
                url_success_count += 1
                star = star[0].split()
                stars.append(star[0])
                print(line[1])
                if not topic:
                    pass
                else:
                    repo_accessed_count += 1
                    for tp in topic:
                        tp = " ".join(re.findall("[a-zA-Z]+", tp))
                        topics.append(tp)
            except:
                print("failed to load page.")


    print(stars)
    print("number of repos:", repo_count)
    print("number of repos accessed:",url_success_count)
    print("number of repos that have topic tag:", repo_accessed_count)
    print("length of topics:", len(topics))



    # with open('./analysis_data/topics.pkl', 'wb') as pf:
    #     pickle.dump(topics, pf)


def nodeCount(file):
    ast_count = 0
    node_counts = []
    with open(file) as fp:
        for line in fp:
            types = re.findall('"type"',line)
            #type_value = re.findall('"type":"[a-zA-Z]+"', line)
            node_count = len(types)
            node_counts.append(node_count)
            ast_count += 1

    print("number of ASTs:", ast_count)
    print("mean of the number of nodes:", statistics.mean(node_counts))
    print("median of the number of nodes:", statistics.median(node_counts))
    print("max node:", max(node_counts))
    print("min node:", min(node_counts))
    sns.distplot(node_counts, hist=False)
    plt.show()

def displayTopNodes(file):
    nodes = []
    nodes_count = []
    count = 0
    with open(file) as json_file:
        data = json.load(json_file)
        for key in data:
            nodes.append(key)
            nodes_count.append(data[key])
            count += 1
            if count == 30: break

    plt.bar(nodes, nodes_count)
    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-large'
    )
    plt.show()

def main():

    #getLibraries('./../Dataset/python100k_train.txt')
    #listCount('./analysis_data/libraries.pkl', 20)
    #getContext('./../Dataset/github_repos.txt')
    #listCount('./analysis_data/topics.pkl',30)
    #nodeCount('./../dataset_python_150k/python50k_eval.json')
    #displayTopNodes('./analysis_data/vocab.json')

if __name__ == "__main__":
    main()
