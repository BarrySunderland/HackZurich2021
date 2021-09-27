# predictive_maintenance extension to QGIS
In order to visualise the results of the model of the hackathon we used a basic plugin to QGIS. As it was a tool I used during that hackathon and there was interest in seeing it I've uploaded it here.

To use this you will need to download the software called QGIS, which is a widely used open source GIS platform. It is well maintained, funded by private companies and governments from around the world and has an estimated community of over 200K+
To install the plugin you need to:

- Install QGIS
- navigate to the `/predictive_maintenance folder`
- install the tool pb_tool with `pip3 install pb_tool`
- then run `pb_tool deploy`

![QGIS screen shot](https://github.com/BarrySunderland/HackZurich2021/raw/QGIS_extension/predictive_maintenance/horizonDataView.png)

This will compile a fresh version of the plugin into your qgis system. If you would like to continue to work with this app then each time you make a change your want to deploy you should run 
- `pb_tool clean`

The tool will now be available in the vector tools menu. If you would like to more widely available at any point then there is a process by which you can include it in the plugin store of qgis. To try this out go to the plugin menu and experiment with downloading other plugins.