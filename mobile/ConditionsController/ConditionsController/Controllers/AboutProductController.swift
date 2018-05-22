//
//  AboutProductController.swift
//  ConditionsController
//
//  Created by olderor on 21.05.2018.
//  Copyright © 2018 Bohdan Yevchenko. All rights reserved.
//

import UIKit

class AboutProductController: UITableViewController {

  @IBOutlet weak var statusLabel: UILabel!
  @IBOutlet weak var identifierLabel: UILabel!
  @IBOutlet weak var nameLabel: UILabel!
  @IBOutlet weak var productTypeLabel: UILabel!
  @IBOutlet weak var createdDateLabel: UILabel!
  @IBOutlet weak var organizationLabel: UILabel!
  @IBOutlet weak var trackingDeviceLabel: UILabel!
  
  @IBAction func onBackBarButtonItemTouch(_ sender: UIBarButtonItem) {
    self.dismiss(animated: true, completion: nil)
  }
  
  var productId: String! = "3"
  var productModel: ProductModel!
  
  
  override func viewWillAppear(_ animated: Bool) {
    Server.getProductInfo(productId: productId, onSuccess: onDataRetrieved)
  }
  
  func onDataRetrieved(model: ProductModel?) {
    if model == nil {
      showError(errorMessage: "Internet connection error.")
      return
    }
    productModel = model
    if !productModel.successed {
      if productModel.error != nil {
        showError(errorMessage: productModel.error!)
      } else {
        showError(errorMessage: "Internet connection error.")
      }
      return
    }
    
    statusLabel.text = productModel.status
    if productModel.id != nil {
      identifierLabel.text = "\(productModel.id!)"
    }
    nameLabel.text = productModel.name
    productTypeLabel.text = productModel.productTypeName
    createdDateLabel.text = productModel.dateCreated
    organizationLabel.text = productModel.organizationName
    if productModel.trackingDeviceId != nil {
      trackingDeviceLabel.text = "\(productModel.trackingDeviceId!)"
    }
    
    switch productModel.statusEn {
    case "spoiled", "expired":
      statusLabel.textColor = UIColor.red
      break
    default:
      break
    }
  }
  
  func showError(errorMessage: String) {
    let alert = UIAlertController(title: "Error", message: errorMessage, preferredStyle: .alert)
    alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
    present(alert, animated: true, completion: nil)
  }
  
  override func tableView(_ tableView: UITableView, willSelectRowAt indexPath: IndexPath) -> IndexPath? {
    if indexPath.row == 7 { //indexPath.row == 3 || todo
      return indexPath
    }
    return nil
  }
  
  override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
    tableView.deselectRow(at: indexPath, animated: true)
    if indexPath.row == 7 {
      let chartController = self.storyboard?.instantiateViewController(withIdentifier: "conditions") as! ChartController
      chartController.productModel = productModel
      self.navigationController?.pushViewController(chartController, animated: true)
    }
  }
}
