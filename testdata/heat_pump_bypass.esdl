<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="4e7bf07a-c2de-4898-a363-6b45f91df62b" description="" esdlVersion="v2207" name="Untitled EnergySystem with return network" version="8">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="c615f17e-c077-48c4-8a78-6ae05f8a908f">
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="f61a1799-bf04-416a-b15e-93097722ada7">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" multiplier="MEGA" unit="WATT" description="Power in MW"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" id="12c481c0-f81e-49b6-9767-90457684d24a" multiplier="KILO" unit="WATTHOUR" description="Energy in kWh"/>
    </quantityAndUnits>
    <carriers xsi:type="esdl:Carriers" id="c27258b1-f4f6-4e09-a77a-ce466dbd82d2">
      <carrier xsi:type="esdl:HeatCommodity" supplyTemperature="60.0" name="HeatSupply" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" name="HeatReturn" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
      <carrier xsi:type="esdl:HeatCommodity" id="34859981-9666-43f0-9ce4-ebf64bf075d7" name="Secondaryheat" supplyTemperature="50.0" returnTemperature="30.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="c24910dd-b95d-4d15-9e30-07503fd99967" name="secondaryheat_2" supplyTemperature="50.0" returnTemperature="30.0"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="a357cbbe-f277-42b1-8456-cbbadc8ceb2e" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="e4002c22-abd5-43f6-81a8-e6b5f960bfa5">
      <asset xsi:type="esdl:HeatingDemand" id="48f3e425-2143-4dcd-9101-c7e22559e82b" name="HeatingDemand_48f3">
        <port xsi:type="esdl:InPort" id="af0904f7-ba1f-4e79-9040-71e08041601b" name="In" connectedTo="3c924a68-29dc-46a4-8e9f-135915370276" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="e890f65f-80e7-46fa-8c52-5385324bf686" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" connectedTo="7ec99d06-2fdf-4224-a362-5eb489e9307e">
          <profile xsi:type="esdl:InfluxDBProfile" endDate="2019-12-31T22:00:00.000000+0000" id="b77e41bc-a5ca-4823-b467-09872f2b6772" port="443" host="profiles.warmingup.info" filters="" startDate="2018-12-31T23:00:00.000000+0000" database="energy_profiles" measurement="WarmingUp default profiles" field="demand4_MW">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" lat="52.16729234478614" lon="4.594259262084962"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" power="500000.0" id="cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4" name="GenericProducer_cf3d">
        <port xsi:type="esdl:InPort" id="9c258b9d-3149-4720-8931-f4bef1080ec1" name="In" connectedTo="1ace2635-d4fd-4ff7-b296-9c6711758658" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="3c420696-d3b7-40d2-816e-2558c9258739"/>
        <geometry xsi:type="esdl:Point" lat="52.16686460258433" lon="4.593336582183839"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="e64c67bc-5507-4c07-8f27-e88c971b0a46" name="Joint_e64c">
        <port xsi:type="esdl:InPort" id="3c420696-d3b7-40d2-816e-2558c9258739" name="In" connectedTo="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="3c924a68-29dc-46a4-8e9f-135915370276" name="Out" connectedTo="af0904f7-ba1f-4e79-9040-71e08041601b 55d4ea5c-c3f8-4f19-912b-8b6663405692" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <geometry xsi:type="esdl:Point" lat="52.16705873224708" lon="4.594007134437562"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="e518886b-fa13-4ec2-aac6-b0eedefa6d3b" name="Joint_e518">
        <port xsi:type="esdl:InPort" id="7ec99d06-2fdf-4224-a362-5eb489e9307e" name="In" connectedTo="e890f65f-80e7-46fa-8c52-5385324bf686 1f605804-592c-4958-8d3a-8198ea1f31b5" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="1ace2635-d4fd-4ff7-b296-9c6711758658" name="Out" connectedTo="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <geometry xsi:type="esdl:Point" lat="52.16717389351117" lon="4.593690633773805"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="d90ca53c-03cf-4e08-a7a8-a81b5090e7d9" name="HeatPump_d90c" COP="1.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.166476340717985" lon="4.595155119895936"/>
        <port xsi:type="esdl:InPort" id="55d4ea5c-c3f8-4f19-912b-8b6663405692" name="PrimIn" connectedTo="3c924a68-29dc-46a4-8e9f-135915370276" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="1f605804-592c-4958-8d3a-8198ea1f31b5" name="PrimOut" connectedTo="7ec99d06-2fdf-4224-a362-5eb489e9307e" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:InPort" id="681d0faf-f1c0-44f0-b2f6-7a402ed3e336" name="SecIn" connectedTo="e5ace3c3-79e5-4d3f-be60-e2614933db40" carrier="c24910dd-b95d-4d15-9e30-07503fd99967"/>
        <port xsi:type="esdl:OutPort" id="f4a6cc67-a51b-458b-b941-4aa4a32662e8" name="SecOut" connectedTo="fc60bd79-f073-48c9-8f55-d9c5e9f8ad53" carrier="34859981-9666-43f0-9ce4-ebf64bf075d7"/>
      </asset>
      <asset xsi:type="esdl:ATES" id="e8a5a89d-d58e-4991-a920-2a573f2b257c" name="ATES_e8a5" maxChargeRate="11610000.0" maxDischargeRate="11610000.0" aquiferTopDepth="300.0" aquiferThickness="45.0" aquiferMidTemperature="17.0" aquiferNetToGross="1.0" aquiferPorosity="0.3" aquiferPermeability="10000.0" aquiferAnisotropy="4.0" salinity="10000.0" wellCasingSize="13.0" wellDistance="150.0">
        <dataSource xsi:type="esdl:DataSource" name="WarmingUp factsheet: HT-ATES (high)" description="This data was generated using the 'kosten_per_asset.xslx' file in the 'Kentallen' directory of WarmingUp project 1D" attribution=""/>
        <costInformation xsi:type="esdl:CostInformation">
          <investmentCosts xsi:type="esdl:SingleValue" value="2333594.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR" id="05da15c0-19dd-478b-8deb-facdca776158"/>
          </investmentCosts>
          <variableOperationalCosts xsi:type="esdl:SingleValue" value="69666.67">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR/yr" perTimeUnit="YEAR" id="c60f06a4-2300-4ce9-ae04-73f4832ddbf2"/>
          </variableOperationalCosts>
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" value="115472.22">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR/yr" perTimeUnit="YEAR" id="cdabd29a-45a7-4b2d-95f9-c983c1f9d6b2"/>
          </fixedMaintenanceCosts>
          <fixedOperationalCosts xsi:type="esdl:SingleValue" value="30000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" description="Cost in EUR/yr" perTimeUnit="YEAR" id="611747a6-c9fb-4653-9e93-eb4d41583700"/>
          </fixedOperationalCosts>
        </costInformation>
        <geometry xsi:type="esdl:Point" lat="52.16626650932859" lon="4.595051854848863"/>
        <port xsi:type="esdl:InPort" id="fc60bd79-f073-48c9-8f55-d9c5e9f8ad53" name="In" connectedTo="f4a6cc67-a51b-458b-b941-4aa4a32662e8" carrier="34859981-9666-43f0-9ce4-ebf64bf075d7"/>
        <port xsi:type="esdl:OutPort" id="e5ace3c3-79e5-4d3f-be60-e2614933db40" name="Out" connectedTo="681d0faf-f1c0-44f0-b2f6-7a402ed3e336" carrier="c24910dd-b95d-4d15-9e30-07503fd99967"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
