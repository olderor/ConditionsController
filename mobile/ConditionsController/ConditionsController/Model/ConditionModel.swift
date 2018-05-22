//
//  ConditionModel.swift
//  ConditionsController
//
//  Created by olderor on 22.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import ObjectMapper

class ConditionModel: ErrorModel {
  var id: Int!
  var name: String!
  var description: String!
  var minValue: String!
  var maxValue: String!
  var productTypeId: Int!
  
  var min: Double? {
    return Double(minValue)
  }
  
  var max: Double? {
    return Double(maxValue)
  }
  
  required init?(map: Map){
    super.init(map: map)
  }
  
  override func mapping(map: Map) {
    super.mapping(map: map)
    
    id <- map["id"]
    name <- map["name"]
    description <- map["description"]
    minValue <- map["min_value"]
    maxValue <- map["max_value"]
    productTypeId <- map["product_type_id"]
  }
}
