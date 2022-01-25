def test_general_data_of_fictions_is_correct(self):
    """Teste que les informations communes des fictions sont correctes"""
    res = self.client.get(path=LIST_FICTIONS_URL)

    self.assertEqual(res.data[0]["creation_date"], str(self.author.fictions.first().creation_date))


def test_co_authoring_data_of_fictions_is_correct(self):
    """Teste que les informations de co-autorat des fictions sont correctes"""
    co_author = sample_user()
    co_authored_fiction = sample_fiction(creation_user=co_author, validation_status=3)
    co_authored_fiction.authors.add(self.author)

    res = self.client.get(path=LIST_FICTIONS_URL)

    # TODO - faire un point sur les unittests de serialiseurs pour éléganter tout ça
    self.assertIn(co_authored_fiction, res.data)
    self.assertIn(co_author, res.data[-1]["authors"])


def test_reviewed_and_replied_fictions_data_is_correct(self):
    """Teste que les informations de reviews et leurs réponses sont correctes"""
    reviewed_fiction = sample_fiction(creation_user=self.author, validation_status=3)
    sample_review(reviewed_object=reviewed_fiction)
    replied_fiction = sample_fiction(creation_user=self.author, validation_status=3)
    review = sample_review(reviewed_object=replied_fiction)
    review.review_post.reply(creation_user=self.author, content="test reply")

    res = self.client.get(path=LIST_FICTIONS_URL)

    self.assertEqual(1, res.data[-2]["review_count"])
    self.assertEqual(1, res.data[-1]["reply_count"])


def test_validation_status_data_of_fictions_is_correct(self):
    """Teste que les informations de status de validation des fictions sont correctes"""
    pending_fiction = sample_fiction(creation_user=self.author, validation_status=2)

    res = self.client.get(path=LIST_FICTIONS_URL)

    self.assertEqual(2, res.data[-1]["validation_status"])


def test_publication_status_data_of_fictions_is_correct(self):
    """Teste que les informations de status des fictions sont correctes"""
    abandonned_fiction = sample_fiction(creation_user=self.author, status=3)

    res = self.client.get(path=LIST_FICTIONS_URL)

    self.assertEqual(3, res.data[-1]["status"])