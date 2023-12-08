<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" version="1" id="f520dfe5-2a3c-411e-ba26-6587a0654694" description="" esdlVersion="v2303" name="Untitled EnergySystem">
  <instance xsi:type="esdl:Instance" name="Untitled Instance" id="1317fbff-25c7-41ce-8e94-393beb4081a0">
    <area xsi:type="esdl:Area" id="caac32ec-f14d-4feb-a530-7eab126d6f00" name="Untitled Area">
      <asset xsi:type="esdl:Pipe" length="1433.9" id="220f0058-9645-4f26-9983-a2dd55a72fa1" outerDiameter="0.2" diameter="DN100" name="pipe_with_material" innerDiameter="0.1071">
        <port xsi:type="esdl:InPort" id="58080650-5284-448a-adfa-ba0a987436d0" name="In"/>
        <port xsi:type="esdl:OutPort" id="7d92f2f4-e753-4f82-9712-d8960d21b736" name="Out"/>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" thermalConductivity="52.15" name="steel" id="c041d04e-23f0-455a-b0f1-2a6415fabe8d"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03965">
            <matter xsi:type="esdl:Material" thermalConductivity="0.027" name="PUR" id="84dc8019-fa49-4110-b4bf-9aac6d5b7777"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0032">
            <matter xsi:type="esdl:Material" thermalConductivity="0.4" name="HDPE" id="2d8e6bb6-e361-40a4-873e-212a69080dc7"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.00591789953011" lon="4.343891143798829"/>
          <point xsi:type="esdl:Point" lat="52.006234887089924" lon="4.36483383178711"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="4a7ce6ab-88b3-42ef-86b3-57e7a8e64893">
          <investmentCosts xsi:type="esdl:SingleValue" id="9e13d1dd-9b73-4724-ac78-5742aee68618" name="Combined investment and installation costs" value="936.1">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="METRE" unit="EURO" id="283e5ece-fb95-4dd9-997d-dbb0eadd2d7b" description="Costs in EUR/m" physicalQuantity="COST"/>
          </investmentCosts>
        </costInformation>
        <dataSource xsi:type="esdl:DataSource" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf" name="Logstor Product Catalogue Version 2020.03"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="5253967b-8663-40da-8dde-73b9145277de" name="pipe_without_material" length="1386.8" innerDiameter="0.1">
        <port xsi:type="esdl:InPort" id="aee486e8-4201-48ae-aef3-69cdd6f6c091" name="In"/>
        <port xsi:type="esdl:OutPort" id="d7b101c4-3027-4520-9743-cf4c2835d731" name="Out"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.00221954543817" lon="4.343719482421876"/>
          <point xsi:type="esdl:Point" lat="52.00243088819016" lon="4.363975524902345"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" length="1340.3" id="5e9f5eaa-7357-4c5a-b4ff-baf34825c168" outerDiameter="0.225" diameter="DN125" name="pipe_with_reference_01" innerDiameter="0.1325">
        <port xsi:type="esdl:InPort" id="898b765d-316b-4f31-ab7c-4f2737346bd5" name="In"/>
        <port xsi:type="esdl:OutPort" id="143c8a27-b260-44cd-804a-b44970bebeaf" name="Out"/>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" thermalConductivity="52.15" name="steel" id="d9b62340-9a80-48e5-a6c7-fa9000e950a1"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03925">
            <matter xsi:type="esdl:Material" thermalConductivity="0.027" name="PUR" id="f42fd948-81eb-4397-9bc6-3d79548b6e50"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0034">
            <matter xsi:type="esdl:Material" thermalConductivity="0.4" name="HDPE" id="24f9f844-56e5-4cc5-886d-8b551567a4b3"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.007080176273114" lon="4.371013641357423"/>
          <point xsi:type="esdl:Point" lat="52.00750281487767" lon="4.390583038330079"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="70ecd2d8-0f2c-43cb-ba3f-e4c2a6521b00">
          <investmentCosts xsi:type="esdl:SingleValue" id="1be86d74-635a-4a59-9f9c-e5c556480d2a" name="Combined investment and installation costs" value="1026.9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="METRE" unit="EURO" id="a1293714-ed26-4601-bab0-3e4bf34e22ec" description="Costs in EUR/m" physicalQuantity="COST"/>
          </investmentCosts>
        </costInformation>
        <dataSource xsi:type="esdl:DataSource" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf" name="Logstor Product Catalogue Version 2020.03"/>
      </asset>
      <asset xsi:type="esdl:Pipe" length="1210.3" id="e91dec02-ca7e-4f6d-af13-70faa87c56a9" outerDiameter="0.225" diameter="DN125" name="pipe_with_reference_02" innerDiameter="0.1325">
        <port xsi:type="esdl:InPort" id="20e977af-64c1-45a1-88f1-c65d0ba013ed" name="In"/>
        <port xsi:type="esdl:OutPort" id="a1b4846f-f33c-4639-8944-65718a280cfa" name="Out"/>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0036">
            <matter xsi:type="esdl:Material" thermalConductivity="52.15" name="steel" id="d9b62340-9a80-48e5-a6c7-fa9000e950a1"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.03925">
            <matter xsi:type="esdl:Material" thermalConductivity="0.027" name="PUR" id="f42fd948-81eb-4397-9bc6-3d79548b6e50"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0034">
            <matter xsi:type="esdl:Material" thermalConductivity="0.4" name="HDPE" id="24f9f844-56e5-4cc5-886d-8b551567a4b3"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.002853570700445" lon="4.3720436096191415"/>
          <point xsi:type="esdl:Point" lat="52.002853570700445" lon="4.389724731445313"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="4dce29ae-7f72-4cda-9b27-bceb3b626624">
          <investmentCosts xsi:type="esdl:SingleValue" id="1be86d74-635a-4a59-9f9c-e5c556480d2a" name="Combined investment and installation costs" value="1026.9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="METRE" unit="EURO" id="a1293714-ed26-4601-bab0-3e4bf34e22ec" description="Costs in EUR/m" physicalQuantity="COST"/>
          </investmentCosts>
        </costInformation>
        <dataSource xsi:type="esdl:DataSource" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf" name="Logstor Product Catalogue Version 2020.03"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
