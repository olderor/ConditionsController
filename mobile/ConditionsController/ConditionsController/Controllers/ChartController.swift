//
//  ChartController.swift
//  ConditionsController
//
//  Created by olderor on 22.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import UIKit
import SwiftChart

class ChartController: UITableViewController {
  var chartViews = [Chart]()
  var chartIdForConditionDict = [Int : Int]()
  var productModel: ProductModel!
  var timer: Timer!
  var lastDateString: String?
  var lastDate: Date!
  
  override func viewDidLoad() {
    for i in 0..<productModel.conditions.count {
      chartViews.append(Chart())
      chartIdForConditionDict.updateValue(i, forKey: productModel.conditions[i].id!)
    }
    addStatuses(productModel)
    timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(ChartController.update), userInfo: nil, repeats: true)
  }
  
  @objc func update() {
    Server.getProductTrackings(productId: "\(productModel.id!)", fromDate: lastDateString, onSuccess: addStatuses)
  }
  
  func addStatuses(_ productModel: ProductModel?) {
    if productModel == nil {
      return
    }
    if productModel!.error != nil {
      print(productModel!.error!)
      return
    }
    productModel!.trackingStatuses.sort(by: { $0.date < $1.date })
    for i in 0..<productModel!.conditions.count {
      let condition = productModel!.conditions[i]
      if let chartId = chartIdForConditionDict[condition.id!] {
        if chartViews[chartId].series.count == 0 {
          chartViews[chartId].add(ChartSeries([]))
          chartViews[chartId].add(ChartSeries([]))
          chartViews[chartId].add(ChartSeries([]))
          chartViews[chartId].series[1].color = UIColor.red
          chartViews[chartId].series[2].color = UIColor.green
          chartViews[chartId].series[1].area = true
          chartViews[chartId].series[2].area = true
          chartViews[chartId].xLabelsFormatter = { _,_ in "" }
        }
        for status in productModel!.trackingStatuses {
          if status.conditionId == condition.id {
            if lastDate == nil || lastDate < status.date {
              lastDate = status.date
              lastDateString = status.dateRecordered
            }
            chartViews[chartId].series[0].data.append((Double(chartViews[chartId].series[0].data.count), status.value))
            if condition.min != nil {
              chartViews[chartId].series[1].data.append((Double(chartViews[chartId].series[1].data.count), condition.min!))
            }
            if condition.max != nil {
              chartViews[chartId].series[2].data.append((Double(chartViews[chartId].series[2].data.count), condition.max!))
            }
          }
        }
        chartViews[chartId].setNeedsDisplay()
      }
    }
  }
  
  override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
    return productModel.conditions.count
  }
  
  override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
    let cell = tableView.dequeueReusableCell(withIdentifier: "chartCell") as! ChartCell
    cell.conditionNameLabel.text = productModel.conditions[indexPath.row].name
    cell.chartContainerView.addSubview(chartViews[indexPath.row])
    chartViews[indexPath.row].frame = CGRect(x: 0, y: 0, width: cell.chartContainerView.frame.width, height: cell.chartContainerView.frame.height)
    
    
    return cell
  }
}
