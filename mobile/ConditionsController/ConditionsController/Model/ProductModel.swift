//
//  ProductModel.swift
//  ConditionsController
//
//  Created by olderor on 22.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import ObjectMapper

class ProductModel: ErrorModel {
  var id: String!
  var name: String!
  var organizationId: String!
  var trackingDeviceId: String!
  var productTypeId: String!
  var statusEn: String!
  var status: String!
  var dateCreated: String!
  var organizationName: String!
  var productTypeName: String!
  var trackingStatuses: String!
  var conditions: String!
  
  required init?(map: Map){
    super.init(map: map)
  }
  
  override func mapping(map: Map) {
    super.mapping(map: map)
    
    id <- map["id"]
    name <- map["name"]
    organizationId <- map["organization_id"]
    trackingDeviceId <- map["tracking_device_id"]
    productTypeId <- map["product_type_id"]
    statusEn <- map["status_en"]
    status <- map["status"]
    dateCreated <- map["date_created"]
    organizationName <- map["organization_name"]
    productTypeName <- map["product_type_name"]
    trackingStatuses <- map["tracking_statuses"]
    conditions <- map["conditions"]
  }
}
