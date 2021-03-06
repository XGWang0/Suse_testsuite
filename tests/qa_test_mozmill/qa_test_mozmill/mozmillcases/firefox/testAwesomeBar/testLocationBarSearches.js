/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is MozMill Test code.
 *
 * The Initial Developer of the Original Code is the Mozilla Foundation.
 * Portions created by the Initial Developer are Copyright (C) 2009
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *   Tracy Walker <twalker@mozilla.com>
 *   Henrik Skupin <hskupin@mozilla.com>
 *   Mark Locklear <marklocklear@gmail.com>
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * **** END LICENSE BLOCK *****/

// Include necessary modules
var RELATIVE_ROOT = '../../shared-modules';
var MODULE_REQUIRES = ['PrefsAPI', 'ToolbarAPI'];

const gTimeout = 5000;

const localTestFolder = collector.addHttpResource('../test-files/');
const prefName = "keyword.URL";

var setupModule = function(module) {
  controller = mozmill.getBrowserController();
  locationBar =  new ToolbarAPI.locationBar(controller);

  PrefsAPI.preferences.setPref(prefName, localTestFolder + "search/searchresults.html?q=");
}

var teardownModule = function() {
  PrefsAPI.preferences.clearUserPref(prefName);
}

/**
 * Check search in location bar for non-domain search terms (feeling lucky search)
 */
var testLocationBarSearches = function() {
  var testString = "Mozilla Firefox";

  controller.open("about:blank");
  controller.waitForPageLoad();

  locationBar.loadURL(testString);
  controller.waitForPageLoad();

  // Check for presense of search term in return results count
  var resultsStringCheck = new elementslib.ID(controller.tabs.activeTab, "term");
  controller.assertText(resultsStringCheck, testString);
}

/**
 * Map test functions to litmus tests
 */
// testLocationBarSearches.meta = {litmusids : [6040]};
