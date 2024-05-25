import json


def read_jsonl(filename):
    data = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            data.append(record)
    return data


def get_documents(file_path):

    data = read_jsonl(file_path)
    print(len(data))

    all_documents = []
    all_overview = ""
    metadata = {}
    save_overview_error = {}
    for doc in data:
        if (
            doc["resume_doc"]
            != "Evaluation Only. Created with Aspose.Cells for Python via Java.Copyright 2003 - 2024 Aspose Pty Ltd."
        ):
            if "page_label" not in doc["metadata"]:
                all_documents.append(doc)
            if "page_label" in doc["metadata"]:
                if int(doc["metadata"]["page_label"]) == 1:
                    if all_overview != "":
                        save_overview_error["metadata"] = metadata
                        save_overview_error["overview_CV"] = all_overview
                        all_documents.append(save_overview_error)
                        save_overview_error = {}
                    all_overview = ""
                    all_overview += doc["overview_CV"]
                elif int(doc["metadata"]["page_label"]) >= 2:
                    all_overview += doc["overview_CV"]
                    metadata = doc["metadata"]
    return all_documents
