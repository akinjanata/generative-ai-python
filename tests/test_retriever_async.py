# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections
import copy
import math
import unittest
import unittest.mock as mock

import google.ai.generativelanguage as glm

from google.generativeai import retriever
from google.generativeai import client as client_lib
from google.generativeai.types import retriever_types as retriever_service
from absl.testing import absltest
from absl.testing import parameterized


class AsyncTests(parameterized.TestCase, unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = unittest.mock.AsyncMock()

        client_lib._client_manager.clients["retriever_async"] = self.client

        def add_client_method(f):
            name = f.__name__
            setattr(self.client, name, f)
            return f

        self.observed_requests = []
        self.responses = collections.defaultdict(list)

        @add_client_method
        async def create_corpus(
            request: glm.CreateCorpusRequest,
        ) -> glm.Corpus:
            self.observed_requests.append(request)
            return glm.Corpus(
                name="corpora/demo_corpus",
                display_name="demo_corpus",
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def get_corpus(
            request: glm.GetCorpusRequest,
        ) -> glm.Corpus:
            self.observed_requests.append(request)
            return glm.Corpus(
                name="corpora/demo_corpus",
                display_name="demo_corpus",
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def update_corpus(request: glm.UpdateCorpusRequest) -> glm.Corpus:
            self.observed_requests.append(request)
            return glm.Corpus(
                name="corpora/demo_corpus",
                display_name="demo_corpus_1",
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def list_corpora(request: glm.ListCorporaRequest) -> glm.ListCorporaResponse:
            self.observed_requests.append(request)

            async def results():
                yield glm.Corpus(
                    name="corpora/demo_corpus_1",
                    display_name="demo_corpus_1",
                    create_time="2000-01-01T01:01:01.123456Z",
                    update_time="2000-01-01T01:01:01.123456Z",
                )
                yield glm.Corpus(
                    name="corpora/demo_corpus_2",
                    display_name="demo_corpus_2",
                    create_time="2000-01-01T01:01:01.123456Z",
                    update_time="2000-01-01T01:01:01.123456Z",
                )

            return results()

        @add_client_method
        async def query_corpus(
            request: glm.QueryCorpusRequest,
        ) -> glm.QueryCorpusResponse:
            self.observed_requests.append(request)
            return glm.QueryCorpusResponse(
                relevant_chunks=[
                    glm.RelevantChunk(
                        chunk_relevance_score=0.08,
                        chunk=glm.Chunk(
                            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                            data={"string_value": "This is a demo chunk."},
                            custom_metadata=[],
                            state=0,
                            create_time="2000-01-01T01:01:01.123456Z",
                            update_time="2000-01-01T01:01:01.123456Z",
                        ),
                    )
                ]
            )

        @add_client_method
        async def delete_corpus(request: glm.DeleteCorpusRequest) -> None:
            self.observed_requests.append(request)

        @add_client_method
        async def create_document(
            request: glm.CreateDocumentRequest,
        ) -> retriever_service.Document:
            self.observed_requests.append(request)
            return glm.Document(
                name="corpora/demo_corpus/documents/demo_doc",
                display_name="demo_doc",
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def get_document(
            request: glm.GetDocumentRequest,
        ) -> retriever_service.Document:
            self.observed_requests.append(request)
            return glm.Document(
                name="corpora/demo_corpus/documents/demo_doc",
                display_name="demo_doc",
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def update_document(
            request: glm.UpdateDocumentRequest,
        ) -> glm.Document:
            self.observed_requests.append(request)
            return glm.Document(
                name="corpora/demo_corpus/documents/demo_doc",
                display_name="demo_doc_1",
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def list_documents(
            request: glm.ListDocumentsRequest,
        ) -> glm.ListDocumentsResponse:
            self.observed_requests.append(request)

            async def results():
                yield glm.Document(
                    name="corpora/demo_corpus/documents/demo_doc_1",
                    display_name="demo_doc_1",
                    create_time="2000-01-01T01:01:01.123456Z",
                    update_time="2000-01-01T01:01:01.123456Z",
                )
                yield glm.Document(
                    name="corpora/demo_corpus/documents/demo_doc_2",
                    display_name="demo_doc_2",
                    create_time="2000-01-01T01:01:01.123456Z",
                    update_time="2000-01-01T01:01:01.123456Z",
                )

            return results()

        @add_client_method
        async def delete_document(
            request: glm.DeleteDocumentRequest,
        ) -> None:
            self.observed_requests.append(request)

        @add_client_method
        async def query_document(
            request: glm.QueryDocumentRequest,
        ) -> glm.QueryDocumentResponse:
            self.observed_requests.append(request)
            return glm.QueryDocumentResponse(
                relevant_chunks=[
                    glm.RelevantChunk(
                        chunk_relevance_score=0.08,
                        chunk=glm.Chunk(
                            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                            data={"string_value": "This is a demo chunk."},
                            custom_metadata=[],
                            state=0,
                            create_time="2000-01-01T01:01:01.123456Z",
                            update_time="2000-01-01T01:01:01.123456Z",
                        ),
                    )
                ]
            )

        @add_client_method
        async def create_chunk(
            request: glm.CreateChunkRequest,
        ) -> retriever_service.Chunk:
            self.observed_requests.append(request)
            return glm.Chunk(
                name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                data={"string_value": "This is a demo chunk."},
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def batch_create_chunks(
            request: glm.BatchCreateChunksRequest,
        ) -> glm.BatchCreateChunksResponse:
            self.observed_requests.append(request)
            return glm.BatchCreateChunksResponse(
                chunks=[
                    glm.Chunk(
                        name="corpora/demo_corpus/documents/demo_doc/chunks/dc",
                        data={"string_value": "This is a demo chunk."},
                        create_time="2000-01-01T01:01:01.123456Z",
                        update_time="2000-01-01T01:01:01.123456Z",
                    ),
                    glm.Chunk(
                        name="corpora/demo_corpus/documents/demo_doc/chunks/dc1",
                        data={"string_value": "This is another demo chunk."},
                        create_time="2000-01-01T01:01:01.123456Z",
                        update_time="2000-01-01T01:01:01.123456Z",
                    ),
                ]
            )

        @add_client_method
        async def get_chunk(
            request: glm.GetChunkRequest,
        ) -> retriever_service.Chunk:
            self.observed_requests.append(request)
            return glm.Chunk(
                name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                data={"string_value": "This is a demo chunk."},
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def list_chunks(
            request: glm.ListChunksRequest,
        ) -> glm.ListChunksResponse:
            self.observed_requests.append(request)

            async def results():
                yield glm.Chunk(
                    name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                    data={"string_value": "This is a demo chunk."},
                    create_time="2000-01-01T01:01:01.123456Z",
                    update_time="2000-01-01T01:01:01.123456Z",
                )
                yield glm.Chunk(
                    name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk_1",
                    data={"string_value": "This is another demo chunk."},
                    create_time="2000-01-01T01:01:01.123456Z",
                    update_time="2000-01-01T01:01:01.123456Z",
                )

            return results()

        @add_client_method
        async def update_chunk(request: glm.UpdateChunkRequest) -> glm.Chunk:
            self.observed_requests.append(request)
            return glm.Chunk(
                name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                data={"string_value": "This is an updated demo chunk."},
                create_time="2000-01-01T01:01:01.123456Z",
                update_time="2000-01-01T01:01:01.123456Z",
            )

        @add_client_method
        async def batch_update_chunks(
            request: glm.BatchUpdateChunksRequest,
        ) -> glm.BatchUpdateChunksResponse:
            self.observed_requests.append(request)
            return glm.BatchUpdateChunksResponse(
                chunks=[
                    glm.Chunk(
                        name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                        data={"string_value": "This is an updated chunk."},
                        create_time="2000-01-01T01:01:01.123456Z",
                        update_time="2000-01-01T01:01:01.123456Z",
                    ),
                    glm.Chunk(
                        name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk_1",
                        data={"string_value": "This is another updated chunk."},
                        create_time="2000-01-01T01:01:01.123456Z",
                        update_time="2000-01-01T01:01:01.123456Z",
                    ),
                ]
            )

        @add_client_method
        async def delete_chunk(
            request: glm.DeleteChunkRequest,
        ) -> None:
            self.observed_requests.append(request)

        @add_client_method
        async def batch_delete_chunks(
            request: glm.BatchDeleteChunksRequest,
        ) -> None:
            self.observed_requests.append(request)

    async def test_create_corpus(self, display_name="demo_corpus"):
        x = await retriever.create_corpus_async(display_name=display_name)
        self.assertIsInstance(x, retriever_service.Corpus)
        self.assertEqual("demo_corpus", x.display_name)
        self.assertEqual("corpora/demo_corpus", x.name)

    @parameterized.named_parameters(
        [
            dict(testcase_name="match_corpora_regex", name="corpora/demo_corpus"),
            dict(testcase_name="no_corpora", name="demo_corpus"),
            dict(testcase_name="with_punctuation", name="corpora/demo_corpus*(*)"),
            dict(testcase_name="dash_at_start", name="-demo_corpus"),
        ]
    )
    async def test_create_corpus_names(self, name):
        x = await retriever.create_corpus_async(name=name)
        self.assertEqual("demo_corpus", x.display_name)
        self.assertEqual("corpora/demo_corpus", x.name)

    async def test_get_corpus(self, display_name="demo_corpus"):
        x = await retriever.create_corpus_async(display_name=display_name)
        c = await retriever.get_corpus_async(name=x.name)
        self.assertEqual("demo_corpus", c.display_name)

    async def test_update_corpus(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        update_request = await demo_corpus.update_async(updates={"display_name": "demo_corpus_1"})
        self.assertEqual("demo_corpus_1", demo_corpus.display_name)

    async def test_list_corpora(self):
        result = []
        async for x in retriever.list_corpora_async(page_size=1):
            result.append(x)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    async def test_query_corpus(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        demo_chunk = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        q = await demo_corpus.query_async(query="What kind of chunk is this?")
        self.assertEqual(
            q,
            [
                retriever_service.RelevantChunk(
                    chunk_relevance_score=0.08,
                    chunk=retriever_service.Chunk(
                        name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                        data="This is a demo chunk.",
                        custom_metadata=[],
                        state=0,
                        create_time="2000-01-01T01:01:01.123456Z",
                        update_time="2000-01-01T01:01:01.123456Z",
                    ),
                )
            ],
        )

    async def test_delete_corpus(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        delete_request = await retriever.delete_corpus_async(name="corpora/demo_corpus", force=True)
        self.assertIsInstance(self.observed_requests[-1], glm.DeleteCorpusRequest)

    async def test_create_document(self, display_name="demo_doc"):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        x = await demo_corpus.create_document_async(display_name=display_name)
        self.assertIsInstance(x, retriever_service.Document)
        self.assertEqual("demo_doc", x.display_name)

    @parameterized.named_parameters(
        [
            dict(
                testcase_name="match_document_regex", name="corpora/demo_corpus/documents/demo_doc"
            ),
            dict(testcase_name="no_document", name="corpora/demo_corpus/demo_document"),
            dict(
                testcase_name="with_punctuation", name="corpora/demo_corpus*(*)/documents/demo_doc"
            ),
            dict(testcase_name="dash_at_start", name="-demo_doc"),
        ]
    )
    async def test_create_document_name(self, name):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        x = await demo_corpus.create_document_async(name=name)
        self.assertEqual("corpora/demo_corpus/documents/demo_doc", x.name)
        self.assertEqual("demo_doc", x.display_name)

    async def test_get_document(self, display_name="demo_doc"):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        x = await demo_corpus.create_document_async(display_name=display_name)
        d = await demo_corpus.get_document_async(name=x.name)
        self.assertEqual("demo_doc", d.display_name)

    async def test_update_document(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        update_request = await demo_document.update_async(updates={"display_name": "demo_doc_1"})
        self.assertEqual("demo_doc_1", demo_document.display_name)

    async def test_delete_document(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        demo_doc2 = await demo_corpus.create_document_async(display_name="demo_doc_2")
        delete_request = await demo_corpus.delete_document_async(
            name="corpora/demo_corpus/documents/demo_doc"
        )
        self.assertIsInstance(self.observed_requests[-1], glm.DeleteDocumentRequest)

    async def test_list_documents(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        demo_doc2 = await demo_corpus.create_document_async(display_name="demo_doc_2")
        self.assertLen(list(demo_corpus.list_documents()), 2)

    async def test_query_document(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        demo_chunk = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        q = await demo_document.query_async(query="What kind of chunk is this?")
        self.assertEqual(
            q,
            [
                retriever_service.RelevantChunk(
                    chunk_relevance_score=0.08,
                    chunk=retriever_service.Chunk(
                        name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                        data="This is a demo chunk.",
                        custom_metadata=[],
                        state=0,
                        create_time="2000-01-01T01:01:01.123456Z",
                        update_time="2000-01-01T01:01:01.123456Z",
                    ),
                )
            ],
        )

        print(type(q[0].chunk.create_time))

    async def test_create_chunk(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        self.assertIsInstance(x, retriever_service.Chunk)
        self.assertEqual("corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk", x.name)
        self.assertEqual(retriever_service.ChunkData("This is a demo chunk."), x.data)

    @parameterized.named_parameters(
        [
            dict(
                testcase_name="match_chunk_regex",
                name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            ),
            dict(testcase_name="no_chunk", name="corpora/demo_corpus/demo_document/demo_chunk"),
            dict(
                testcase_name="with_punctuation",
                name="corpora/demo_corpus*(*)/documents/demo_doc/chunks*****/demo_chunk",
            ),
            dict(testcase_name="dash_at_start", name="-demo_chunk"),
        ]
    )
    async def test_create_chunk_name(self, name):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name=name,
            data="This is a demo chunk.",
        )
        self.assertEqual("corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk", x.name)

    @parameterized.named_parameters(
        [
            dict(
                testcase_name="dictionaries",
                chunks=[
                    {
                        "name": "corpora/demo_corpus/documents/demo_doc/chunks/dc",
                        "data": "This is a demo chunk.",
                    },
                    {
                        "name": "corpora/demo_corpus/documents/demo_doc/chunks/dc1",
                        "data": "This is another demo chunk.",
                    },
                ],
            ),
            dict(
                testcase_name="tuples",
                chunks=[
                    (
                        "corpora/demo_corpus/documents/demo_doc/chunks/dc",
                        "This is a demo chunk.",
                    ),
                    (
                        "corpora/demo_corpus/documents/demo_doc/chunks/dc1",
                        "This is another demo chunk.",
                    ),
                ],
            ),
        ]
    )
    async def test_batch_create_chunks(self, chunks):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        chunks = await demo_document.batch_create_chunks_async(chunks=chunks)
        self.assertIsInstance(self.observed_requests[-1], glm.BatchCreateChunksRequest)
        self.assertEqual("This is a demo chunk.", chunks[0].data.string_value)
        self.assertEqual("This is another demo chunk.", chunks[1].data.string_value)

    async def test_get_chunk(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        ch = await demo_document.get_chunk_async(name=x.name)
        self.assertEqual(retriever_service.ChunkData("This is a demo chunk."), ch.data)

    async def test_list_chunks(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        y = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk_1",
            data="This is another demo chunk.",
        )
        chunks = []
        async for chunk in demo_document.list_chunks_async():
            chunks.append(chunk)
        self.assertIsInstance(self.observed_requests[-1], glm.ListChunksRequest)
        self.assertLen(chunks, 2)

    async def test_update_chunk(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        await x.update_async(updates={"data": {"string_value": "This is an updated demo chunk."}})
        self.assertEqual(
            retriever_service.ChunkData("This is an updated demo chunk."),
            x.data,
        )

    @parameterized.named_parameters(
        [
            dict(
                testcase_name="dictionary_of_updates",
                updates={
                    "corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk": {
                        "data": {"string_value": "This is an updated chunk."}
                    },
                    "corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk_1": {
                        "data": {"string_value": "This is another updated chunk."}
                    },
                },
            ),
            dict(
                testcase_name="list_of_tuples",
                updates=[
                    (
                        "corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
                        {"data": {"string_value": "This is an updated chunk."}},
                    ),
                    (
                        "corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk_1",
                        {"data": {"string_value": "This is another updated chunk."}},
                    ),
                ],
            ),
        ],
    )
    async def test_batch_update_chunks_data_structures(self, updates):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        y = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk_1",
            data="This is another demo chunk.",
        )
        update_request = await demo_document.batch_update_chunks_async(chunks=updates)
        self.assertIsInstance(self.observed_requests[-1], glm.BatchUpdateChunksRequest)
        self.assertEqual(
            "This is an updated chunk.", update_request["chunks"][0]["data"]["string_value"]
        )
        self.assertEqual(
            "This is another updated chunk.", update_request["chunks"][1]["data"]["string_value"]
        )

    async def test_delete_chunk(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        delete_request = await demo_document.delete_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk"
        )
        self.assertIsInstance(self.observed_requests[-1], glm.DeleteChunkRequest)

    async def test_batch_delete_chunks(self):
        demo_corpus = await retriever.create_corpus_async(display_name="demo_corpus")
        demo_document = await demo_corpus.create_document_async(display_name="demo_doc")
        x = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is a demo chunk.",
        )
        y = await demo_document.create_chunk_async(
            name="corpora/demo_corpus/documents/demo_doc/chunks/demo_chunk",
            data="This is another demo chunk.",
        )
        delete_request = await demo_document.batch_delete_chunks_async(chunks=[x.name, y.name])
        self.assertIsInstance(self.observed_requests[-1], glm.BatchDeleteChunksRequest)


if __name__ == "__main__":
    absltest.main()
