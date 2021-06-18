import spacy
def entity_recognition(text):
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    nouns = ""
    for chunk in doc.noun_chunks:
        nouns += chunk.text
        nouns += " "



    # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)
    


    return nouns



# text = ("I want to start a business related to education technology where our platform will be providing high quality courses to different stream students, employees")

# print(entity_recognition(text))
