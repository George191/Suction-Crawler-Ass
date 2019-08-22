from crawler.LiePin import CompanyInfo


class QiChaCha(CompanyInfo):

    def __init__(self):
        super(QiChaCha, self).__init__()

        self.analysis_html()


demo = QiChaCha()

