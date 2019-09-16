class ParserHelper:
    @staticmethod
    def match_name_and_classes(tag, name, cls_names):
        return (
                tag.name == name
                and all(cls_ in tag.get('class') for cls_ in cls_names)
        )

    @classmethod
    def find_exact_one(cls, tag_info, tag_name, cls_names=None):
        if not cls_names:
            cls_names = []
        results = tag_info.find_all(lambda x: cls.match_name_and_classes(x, tag_name, cls_names))
        if len(results) == 1:
            return results[0]
        else:
            raise LookupError(f'found #{len(results)}, not exact one')

