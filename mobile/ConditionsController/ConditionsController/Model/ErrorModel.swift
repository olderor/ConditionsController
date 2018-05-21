//
//  File.swift
//  ConditionsController
//
//  Created by olderor on 22.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//


import ObjectMapper

class ErrorModel: Mappable {
  var error: String?
  
  required init?(map: Map){
    
  }
  
  func mapping(map: Map) {
    error <- map["error"]
  }
  
  var successed: Bool {
    return error != nil
  }
}
