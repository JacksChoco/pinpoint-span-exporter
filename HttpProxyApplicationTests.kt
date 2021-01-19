package im.toss.server.apigateway.integTest

import com.fasterxml.jackson.databind.ObjectMapper
import im.toss.server.apigateway.SpringApplicationTest
import mu.KotlinLogging
import org.assertj.core.api.Assertions
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.MediaType

private val logger = KotlinLogging.logger {}

data class HttpProxyResponse(
        val status: Int,
        val statusText: String,
        val headers: List<Map<String, String>>,
        val body: String
)

class HttpProxyApplicationTests : SpringApplicationTest() {

    @Autowired
    lateinit var testDataHelper: TestDataHelper

    @Autowired
    lateinit var objectMapper: ObjectMapper

    private val rawData = mapOf(
            "time" to "1",
            "syncedTime" to "158278577.6642",
            "appVer" to "4.54.0", "os" to "android",
            "word" to "1fbf1bdbb4df9d36572acee83530e1c6c1be2031e334e1c90e3cbedb91318a52",
            "nword" to "7e6411fc5ec47ef143f89d69a0a28198e68395b3409d80a3df730a6e8d56150e",
            "url" to "https://toss.im",
            "method" to "head",
            "body" to "dummy"
    )

    @Nested
    inner class SuccessCase {
        @Test
        fun httpProxyTest() {
            testDataHelper.webTestClient.post().uri("/proxies/http")
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(testDataHelper.bodyInserter(TestDataHelper.BodyBuilder(mapBody = rawData)))
                    .exchange()
                    .expectStatus()
                    .isOk
                    .expectBody().consumeWith { result ->
                        testDataHelper.decodeResult(result.responseBody) { decodeResult ->
                            val responseBodyString = String(decodeResult.responseBody!!)
                            logger.info("result as string - {}", responseBodyString)

                            val httpProxyResponse = objectMapper.readValue(responseBodyString, HttpProxyResponse::class.java)
                            logger.info("result as object - {}", httpProxyResponse)

                            Assertions.assertThat(httpProxyResponse.status).isEqualTo(200)
                        }
                    }
        }
    }
}
