//
//  TrackingStatusModel.swift
//  ConditionsController
//
//  Created by olderor on 22.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import ObjectMapper

class TrackingStatusModel: ErrorModel {
  var id: Int!
  var conditionId: Int!
  var productId: Int!
  var trackingDeviceId: Int!
  var value: Double!
  var dateRecordered: String!
  var date: Date!
  
  required init?(map: Map){
    super.init(map: map)
  }
  
  override func mapping(map: Map) {
    super.mapping(map: map)
    
    id <- map["id"]
    conditionId <- map["condition_id"]
    productId <- map["product_id"]
    trackingDeviceId <- map["tracking_device_id"]
    value <- map["value"]
    dateRecordered <- map["date_recordered"]
    
    let dateFormatter = DateFormatter()
    dateFormatter.dateFormat = "yyyy-MM-dd HH:mm:ss.SSSSSS"
    date = dateFormatter.date(from: dateRecordered)!
  }
}
