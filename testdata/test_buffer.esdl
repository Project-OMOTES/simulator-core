<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="Untitled EnergySystem with return network" description="" id="e7b009e1-8e4a-46d0-bb70-d08af7e17be3_with_return_network" esdlVersion="v2507" version="4">
  <instance xsi:type="esdl:Instance" id="e0c9b698-3bf3-47fe-aea0-9a120fa6ee89" name="Untitled Instance">
    <area xsi:type="esdl:Area" id="919c382f-a01d-492a-8290-daa942d03efa" name="Untitled Area">
      <asset xsi:type="esdl:HeatStorage" id="11cc503d-534c-45f6-89dc-d2a3f47299ff" name="HeatStorage_11cc" fillLevel="0.5" maxDischargeRate="100.0" maxChargeRate="100.0" volume="100.0">
        <geometry xsi:type="esdl:Point" lat="51.935712741050864" lon="4.244440197944642" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="47d7c914-90cc-40b0-96e2-4c03634f6d6c" name="In" connectedTo="41e751f5-3c52-4e7d-be91-c7c7c3425c6e" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
        <port xsi:type="esdl:OutPort" id="65c5f555-f82e-4410-96d4-37575a73888d" name="Out" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret" connectedTo="9c6a60d6-915c-4cd7-b7fe-7977249fc8e6"/>
      </asset>
      <asset xsi:type="esdl:HeatProducer" id="6ebb7d15-2e8b-467c-b9f7-2946be37930c" name="HeatProducer_6ebb">
        <geometry xsi:type="esdl:Point" lat="51.93532908025873" lon="4.240947961807252" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="f80344b3-40e3-4e82-8b6c-50efd6194b0e" name="Out" connectedTo="2417963f-bdde-42df-9d38-859b23887cfb" carrier="db75dded-49f5-4d9c-8172-f837b714476e">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand5_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="6ac02ff2-d16d-4e8d-a6cf-108da713f97d" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="93aa23ea-4c5d-4969-97d4-2a4b2720e523"/>
          </profile>
        </port>
        <port xsi:type="esdl:InPort" id="401d9e5d-938d-4dac-9432-13051992ae5d" name="In" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret" connectedTo="98ea8582-a3d8-44a3-a0a2-c558a9c9352c"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="77bf3478-421f-43fc-bbcc-bb6105d5bb95" name="HeatingDemand_77bf">
        <geometry xsi:type="esdl:Point" lat="51.93405900733476" lon="4.247696399688722" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="8e7a5b13-9d0e-4702-8167-2d661b29ea4a" name="In" connectedTo="ccfaacc6-2c7d-4fb9-819e-642f83b26eaa" carrier="db75dded-49f5-4d9c-8172-f837b714476e">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="0.5" measurement="WarmingUp default profiles" field="demand5_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="fff21788-142c-478c-872c-5e7de62a4bd5" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="93aa23ea-4c5d-4969-97d4-2a4b2720e523"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="cf404e50-34ad-459c-8b3b-9c9a14eaf1a3" name="Out" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret" connectedTo="692db8a2-6ec5-4afd-b35e-d6c2da3cec0e"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe1" name="Pipe1" innerDiameter="0.3127" outerDiameter="0.45" diameter="DN300" length="84.54" roughness="0.01" related="Pipe1_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="07d6bb60-0bf8-49ef-a53c-d8e54a5337cb">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="2ec0bb0f-1e4f-472e-b2f7-6b5dcdcb1cf0" value="1962.1">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="b1705132-f33d-42ad-8526-8ee00ef4a5b0"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" name="steel" id="e428b971-e3f6-4bc1-a04e-397447de603f" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.05785">
            <matter xsi:type="esdl:Material" name="PUR" id="47366a4c-6b4a-4ea4-87fd-d892ae26d1c3" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0052">
            <matter xsi:type="esdl:Material" name="HDPE" id="acbd431e-2fbd-444e-9f00-68d2ac333937" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.935534140745425" lon="4.241269826889039"/>
          <point xsi:type="esdl:Point" lat="51.93567305215554" lon="4.24248218536377"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="2417963f-bdde-42df-9d38-859b23887cfb" name="In" connectedTo="f80344b3-40e3-4e82-8b6c-50efd6194b0e" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
        <port xsi:type="esdl:OutPort" id="26db841a-59bd-4eb8-819d-4b69d2be37dc" name="Out" carrier="db75dded-49f5-4d9c-8172-f837b714476e" connectedTo="a596648e-43d3-45e5-8c41-ab2d2cbd8d58"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe2" name="Pipe2" innerDiameter="0.3127" outerDiameter="0.45" diameter="DN300" length="90.21" roughness="0.01" related="Pipe2_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="07d6bb60-0bf8-49ef-a53c-d8e54a5337cb">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="2ec0bb0f-1e4f-472e-b2f7-6b5dcdcb1cf0" value="1962.1">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="b1705132-f33d-42ad-8526-8ee00ef4a5b0"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" name="steel" id="e428b971-e3f6-4bc1-a04e-397447de603f" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.05785">
            <matter xsi:type="esdl:Material" name="PUR" id="47366a4c-6b4a-4ea4-87fd-d892ae26d1c3" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0052">
            <matter xsi:type="esdl:Material" name="HDPE" id="acbd431e-2fbd-444e-9f00-68d2ac333937" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.93567305215554" lon="4.24248218536377"/>
          <point xsi:type="esdl:Point" lat="51.93580534833677" lon="4.243780374526978"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="beacdc3c-7215-40d2-ba46-88821f0ff21c" name="In" carrier="db75dded-49f5-4d9c-8172-f837b714476e" connectedTo="046d2b15-1ede-4010-a333-3768722b43cb"/>
        <port xsi:type="esdl:OutPort" id="41e751f5-3c52-4e7d-be91-c7c7c3425c6e" name="Out" connectedTo="47d7c914-90cc-40b0-96e2-4c03634f6d6c" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="f0d6617d-9ec5-482f-9599-83657ac5c349" name="Joint_f0d6">
        <port xsi:type="esdl:InPort" id="a596648e-43d3-45e5-8c41-ab2d2cbd8d58" name="In" connectedTo="26db841a-59bd-4eb8-819d-4b69d2be37dc" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
        <port xsi:type="esdl:OutPort" id="046d2b15-1ede-4010-a333-3768722b43cb" name="Out" connectedTo="beacdc3c-7215-40d2-ba46-88821f0ff21c 37c214b2-a33b-4640-ae12-901c01268d96" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
        <geometry xsi:type="esdl:Point" lat="51.93567305215554" lon="4.24248218536377"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe3" name="Pipe3" innerDiameter="0.3127" outerDiameter="0.45" diameter="DN300" length="371.5" roughness="0.01" related="Pipe3_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <costInformation xsi:type="esdl:CostInformation" id="ef39fe51-120f-41de-b93e-63a71ad6c60c">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="a51dd204-256d-4c48-9fe4-cd5baa739b18" value="1962.1">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="00c72062-f276-491b-b48f-2ae40e31123d"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" name="steel" id="036df6f3-f03e-4f52-8b8e-5c5e0c9957bd" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.05785">
            <matter xsi:type="esdl:Material" name="PUR" id="596b74ed-5354-4c7d-8cd3-ad7976ebb2fd" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0052">
            <matter xsi:type="esdl:Material" name="HDPE" id="8a525903-700d-49f3-a199-0e3d75116e2f" thermalConductivity="0.4"/>
          </component>
        </material>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="51.93567305215554" lon="4.24248218536377"/>
          <point xsi:type="esdl:Point" lat="51.93410531270822" lon="4.247267246246339"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="37c214b2-a33b-4640-ae12-901c01268d96" name="In" connectedTo="046d2b15-1ede-4010-a333-3768722b43cb" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
        <port xsi:type="esdl:OutPort" id="ccfaacc6-2c7d-4fb9-819e-642f83b26eaa" name="Out" connectedTo="8e7a5b13-9d0e-4702-8167-2d661b29ea4a" carrier="db75dded-49f5-4d9c-8172-f837b714476e"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="cb46ee82-69b8-4bf9-befb-ebabdc16f71b" name="Joint_f0d6_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.93576305224554" lon="4.241199717972444"/>
        <port xsi:type="esdl:OutPort" id="87607cd3-4dbc-4940-a879-adf935a8e025" name="ret_port" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret" connectedTo="5819a592-638f-450f-a5bc-7377ad796197"/>
        <port xsi:type="esdl:InPort" id="1a99e903-841d-41da-b473-c0343ee297c8" name="ret_port" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret" connectedTo="1514cadf-e297-4720-85e9-c1f96bfe2734 a3a0a6fe-795f-45e5-bbf0-45a2a2a7f919"/>
      </asset>
      <asset xsi:type="esdl:Pipe" innerDiameter="0.3127" outerDiameter="0.45" length="84.54" roughness="0.01" diameter="DN300" id="Pipe1_ret" name="Pipe1_ret" related="Pipe1">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.93576305224554" lon="4.241199717972444"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.93562414083542" lon="4.239985570549223"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="5819a592-638f-450f-a5bc-7377ad796197" name="In_ret" connectedTo="87607cd3-4dbc-4940-a879-adf935a8e025" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
        <port xsi:type="esdl:OutPort" id="98ea8582-a3d8-44a3-a0a2-c558a9c9352c" name="Out_ret" connectedTo="401d9e5d-938d-4dac-9432-13051992ae5d" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" innerDiameter="0.3127" outerDiameter="0.45" length="90.21" roughness="0.01" diameter="DN300" id="Pipe2_ret" name="Pipe2_ret" related="Pipe2">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.93589534842677" lon="4.242499606240577"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.93576305224554" lon="4.241199717972444"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="9c6a60d6-915c-4cd7-b7fe-7977249fc8e6" name="In_ret" connectedTo="65c5f555-f82e-4410-96d4-37575a73888d" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
        <port xsi:type="esdl:OutPort" id="1514cadf-e297-4720-85e9-c1f96bfe2734" name="Out_ret" connectedTo="1a99e903-841d-41da-b473-c0343ee297c8" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" innerDiameter="0.3127" outerDiameter="0.45" length="371.5" roughness="0.01" diameter="DN300" id="Pipe3_ret" name="Pipe3_ret" related="Pipe3">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.93419531279822" lon="4.245964293595001"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.93576305224554" lon="4.241199717972444"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="692db8a2-6ec5-4afd-b35e-d6c2da3cec0e" name="In_ret" connectedTo="cf404e50-34ad-459c-8b3b-9c9a14eaf1a3" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
        <port xsi:type="esdl:OutPort" id="a3a0a6fe-795f-45e5-bbf0-45a2a2a7f919" name="Out_ret" connectedTo="1a99e903-841d-41da-b473-c0343ee297c8" carrier="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="baf7cbf6-e005-42cf-b346-438dac463f48">
    <carriers xsi:type="esdl:Carriers" id="3a0d84a3-cbb2-4087-89d3-87865568b349">
      <carrier xsi:type="esdl:HeatCommodity" id="db75dded-49f5-4d9c-8172-f837b714476e" name="Heat" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="50.0" name="Heat_ret" id="db75dded-49f5-4d9c-8172-f837b714476e_ret"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="5bb55027-3f0d-4cc1-b4b0-3c3d9d1cd19c">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
