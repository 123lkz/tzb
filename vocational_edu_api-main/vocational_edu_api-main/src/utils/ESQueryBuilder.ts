import { ObjectKeys } from '@havenzhang/clover/dist/src/utils/Tools'

export class ESQueryBuilder {
  boolQuery: Record<string, any> = {}

  addShouldQuery(query: any) {
    if (!this.boolQuery.should) {
      this.boolQuery.should = []
      this.boolQuery.minimum_should_match = 1
    }
    this.boolQuery.should.push(query)
  }

  addMustQuery(query: any) {
    if (!this.boolQuery.must) {
      this.boolQuery.must = []
    }
    this.boolQuery.must.push(query)
  }

  toQuery() {
    if (ObjectKeys(this.boolQuery).length > 0) {
      return {
        bool: this.boolQuery
      }
    }
    return {
      match_all: {}
    }
  }
}
